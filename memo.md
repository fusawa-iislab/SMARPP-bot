dbの使い方注意
chatbotsをchatroomで持たなくても



user-inputの形
```
{'user': 'U09217G8XPZ', 'type': 'message', 'ts': '1753238392.261129', 'client_msg_id': 'ba8b0bd0-4164-4116-9a34-1d4314978ddc', 'text': 'test/test', 'team': 'T09217G89E3', 'blocks': [{'type': 'rich_text', 'block_id': '0veey', 'elements': [{'type': 'rich_text_section', 'elements': [{'type': 'text', 'text': 'test/test'}]}]}], 'channel': 'C0929U6PNJJ', 'event_ts': '1753238392.261129', 'channel_type': 'group'}
```
bot-responseの形
```
{'bot_profile': {'id': 'B094D5C21HD', 'deleted': False, 'name': 'ファシリテータ', 'updated': 1751950420, 'app_id': 'A094TTNSV9A', 'user_id': 'U094D5C2939', 'icons': {'image_36': 'https://a.slack-edge.com/80588/img/plugins/app/bot_36.png', 'image_48': 'https://a.slack-edge.com/80588/img/plugins/app/bot_48.png', 'image_72': 'https://a.slack-edge.com/80588/img/plugins/app/service_72.png'}, 'team_id': 'T09217G89E3'}, 'blocks': [{'type': 'rich_text', 'block_id': 'GFh', 'elements': [{'type': 'rich_text_section', 'elements': [{'type': 'text', 'text': 'こんにちは、皆さん。今日は集まっていただきありがとうございます。では、まず最近の様子について伺いたいと思います。何か気になることや良かったことがあれば教えてください。どうですか？\n\nyugoさん、最近何か変化はありましたか？'}]}]}], 'channel': 'C0929U6PNJJ', 'event_ts': '1753238718.524129', 'channel_type': 'group'}
```