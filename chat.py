from app.graph import graph

print("=" * 60)
print("AI Knowledge Assistant")
print("=" * 60)

while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        break

    result = graph.invoke(
        {
            "question": question
        }
    )

    print("\nAssistant:\n")

    print(result["answer"])