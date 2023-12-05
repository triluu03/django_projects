from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
import numpy as np

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
            board_info = await self.get_board_info()
            previous = board_info["previous"]
            self.size = board_info["size"]
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "join_message",
                    "message": message,
                    "previous": previous
                }
            )
        elif message == "update board":
            board_id = data['board_id']
            row = int(data['row'])
            col = int(data['col'])
            next_move = data['next_move']
            details = np.array(data['details']).reshape(self.size, self.size)
            details[row, col] = next_move
            if checkEndGame(details, row, col):
                await self.reset_board()
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "end_message",
                        "message": "end game",
                        "board_id": board_id
                    }
                )
            else:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "play_message",
                        "message": "play message",
                        "button_id": self.size*row + col,
                    }
                )
        elif message == "save game":
            next_move = data['next_move']
            details = data['details']
            try:
                await self.save_game(next_move, details)
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "save_message",
                        "message": message,
                        "status": "success"
                    }
                )
            except:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "save_message",
                        "message": message,
                        "status": "failed"
                    }
                )

    async def join_message(self, event):
        message = event["message"]
        previous = event["previous"]
        await self.send(text_data=json.dumps({
            "message": message,
            "previous": previous,
        }))

    async def play_message(self, event):
        message = event["message"]
        button_id = event["button_id"]
        await self.send(text_data=json.dumps({
            "message": message,
            "buttonId": button_id
        }))

    async def save_message(self, event):
        message = event["message"]
        status = event["status"]
        await self.send(text_data=json.dumps({
            "message": message,
            "status": status
        }))
    
    async def end_message(self, event):
        message = event["message"]
        board_id = event["board_id"]
        await self.send(text_data=json.dumps({
            "message": message,
            "board_id": board_id
        }))
    
    @database_sync_to_async
    def save_game(self, next_move, details):
        board = Board.objects.get(pk=self.board_id)
        board.details = details
        if next_move == "O":
            board.previous = "X"
        else:
            board.previous = "O"
        board.save()

    @database_sync_to_async
    def get_board_info(self):
        board = Board.objects.get(pk=self.board_id)
        return {
            "previous": board.previous,
            "size": board.size
        }
    
    @database_sync_to_async
    def reset_board(self):
        board = Board.objects.get(pk=self.board_id)
        size = board.size
        board.details = ",".join([""]*(size**2))
        board.previous = "O"
        board.save()