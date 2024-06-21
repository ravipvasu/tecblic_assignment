import asyncio
import json
import websockets


async def test_message_translation():
    uri = "ws://127.0.0.1:8000/ws/chat/room1/"

    # Simulate User 1 (sender)
    async with websockets.connect(uri) as sender_ws:
        # Simulate User 2 (receiver)
        async with websockets.connect(uri) as receiver_ws:
            # Register sender and receiver (assuming session IDs are 1 and 2)
            await sender_ws.send(json.dumps({'type': 'register', 'user_id': 1}))
            await receiver_ws.send(json.dumps({'type': 'register', 'user_id': 2}))

            # Send a message from User 1 to User 2
            message = {
                'sender': 1,
                'receiver': 2,
                'content': 'Today is a nice day!',
                'language': 'en'
            }
            await sender_ws.send(json.dumps(message))

            # Receive the translated message at User 2's end
            response = await receiver_ws.recv()
            translated_message = json.loads(response)

            # Output the translated message
            print('Translated Message:', translated_message)


# Run the test
asyncio.get_event_loop().run_until_complete(test_message_translation())
