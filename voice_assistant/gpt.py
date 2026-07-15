def ask_gpt(messages, model, client):
    response = client.chat.completions.create(
                model = model,
                messages = messages
            )
    return response.choices[0].message.content