import cohere

# Replace 'your-api-key' with your actual Cohere API key
api_key = '23CmI70FiLZIiH5NFN3Dz76tvhMKAx2KfEhG4DYA'
co = cohere.Client(api_key)

data = open("roadmap_data.txt", 'r').read()

response = co.chat(
    chat_history=[],
    message="Act as a programming expert and rewrite given roadmaps into more meaningful and helpful roadmaps for programmers according to the input, only return the output as points of the ordered topics without explaining each one, and at the end add the notes(or the extra advices), keep the response clean and easy to manipulate because I will handle it to send the ordered topics into another service using restFull apis, DON'T add extra explain on each topic, just add the name of each topic" + data,
    # perform web search before answering the question. You can also use your own custom connector.
    connectors=[{"id": "web-search"}],
)

print(response.text)
