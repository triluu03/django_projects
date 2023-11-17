from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
import numpy as np

from django.shortcuts import redirect
from .models import Board
from .helper.check_end_conditions import checkEndGame

class GameConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        print('WebSocket connection established')
        self.board_id = self.scope["url_route"]["kwargs"]["board_id"]
        self.room_group_name = f"board_{self.board_id}"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        print(f"WebSocket connection closed with code: {code}")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(f"Message received: {data}")
        message = data['message']
        
        if message == "join game":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "join_message",
                    "message": message
                }
            )
        elif message == "update board":
            board_id = data['board_id']
            row = data['row']
            col = data['col']
            signal = await self.update_board(board_id, row, col)
            if signal == "continue":
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "play_message",
                        "message": message,
                        "board_id": board_id,
                        "row": row,
                        "col": col
                    }
                ) 
            elif signal == "end":
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "end_message",
                        "message": "end game",
                        "board_id": board_id,
                        "last_row": row,
                        "last_col": col
                    }
                )

    async def join_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({
            "message": message
        }))

    async def play_message(self, event):
        message = event["message"]
        board_id = event["board_id"]
        row = event["row"]
        col = event["col"]
        await self.send(text_data=json.dumps({
            "message": message,
            "board_id": board_id,
            "row": row,
            "col": col
        }))
    
    async def end_message(self, event):
        message = event["message"]
        board_id = event["board_id"]
        row = event["last_row"]
        col = event["last_col"]
        await self.send(text_data=json.dumps({
            "message": message,
            "board_id": board_id,
            "last_row": row,
            "last_col": col
        }))

    @database_sync_to_async
    def update_board(self, board_id, row, col):
        row = int(row)
        col = int(col)
        board = Board.objects.get(pk=board_id)
        size = board.size
        previous = board.previous
        details = np.array(board.details.split(',')).reshape(size, size)
        if previous == "O":
            details[row, col] = "X"
            board.previous = "X"
        else:
            details[row, col] = "O"
            board.previous = "O"
        if checkEndGame(details, row, col):
            board.details = ",".join([""]*(size**2))
            board.previous = "O"
            board.save()
            return "end"
        board.details = ",".join(details.flatten().tolist())
        board.save()
        return "continue"
