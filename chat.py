from app.graph import graph


history = []

print("=" * 70)
print("AI Knowledge Assistant")
print("=" * 70)

while True:

    question = input("\nYou : ")

    if question.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    result = graph.invoke({
        "question": question,
        "chat_history": history
    })

    answer = result["answer"]

    print("\nAssistant\n")
    print(answer)

    if result.get("sources"):

        print("\nSources")

        seen = set()

        for s in result["sources"]:

            source = (
                f"{s['file']} | "
                f"Page {s['page'] + 1}"
            )

            if source not in seen:
                seen.add(source)
                print(source)

    history.append({
        "role": "user",
        "content": question
    })

    history.append({
        "role": "assistant",
        "content": answer
    })
