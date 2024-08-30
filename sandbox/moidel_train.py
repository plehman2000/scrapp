import marimo

__generated_with = "0.6.25"
app = marimo.App(width="medium")


@app.cell
def __():

    dataset = [
        {"input": "John went to the store. He bought some milk.",
         "output": "John went to the store. John bought some milk."},
         
        {"input": "Alice gave Bob her book. He thanked her.",
         "output": "Alice gave Bob Alice's book. Bob thanked Alice."},
         
        {"input": "Michael found his keys. He was relieved.",
         "output": "Michael found Michael's keys. Michael was relieved."},
         
        {"input": "Sarah and Emma went to the park. They enjoyed their time there.",
         "output": "Sarah and Emma went to the park. Sarah and Emma enjoyed their time there."},
         
        {"input": "David called his friend. He asked him for help.",
         "output": "David called David's friend. David asked David's friend for help."},
         
        {"input": "Sophia and John visited their grandparents. They brought gifts.",
         "output": "Sophia and John visited Sophia and John's grandparents. Sophia and John brought gifts."},
         
        {"input": "Emma saw a dog. She wanted to pet it.",
         "output": "Emma saw a dog. Emma wanted to pet the dog."},
         
        {"input": "Bob lost his wallet. He couldn't find it anywhere.",
         "output": "Bob lost Bob's wallet. Bob couldn't find the wallet anywhere."},
         
        {"input": "John and Michael played football. They had a great time.",
         "output": "John and Michael played football. John and Michael had a great time."},
         
        {"input": "Alice cooked dinner for her family. They loved it.",
         "output": "Alice cooked dinner for Alice's family. Alice's family loved the dinner."},
         
        {"input": "David and Sarah took their dog for a walk. They enjoyed the evening.",
         "output": "David and Sarah took David and Sarah's dog for a walk. David and Sarah enjoyed the evening."},
         
        {"input": "Emma wrote a letter to her friend. She sent it yesterday.",
         "output": "Emma wrote a letter to Emma's friend. Emma sent the letter yesterday."},
         
        {"input": "Sophia cleaned her room. She found her missing earring.",
         "output": "Sophia cleaned Sophia's room. Sophia found Sophia's missing earring."},
         
        {"input": "John and Alice went to the movies. They watched a comedy.",
         "output": "John and Alice went to the movies. John and Alice watched a comedy."},
         
        {"input": "Michael helped his sister with her homework. She thanked him.",
         "output": "Michael helped Michael's sister with her homework. Michael's sister thanked Michael."},
         
        {"input": "Sarah and Emma prepared their presentation. They practiced it together.",
         "output": "Sarah and Emma prepared Sarah and Emma's presentation. Sarah and Emma practiced the presentation together."},
         
        {"input": "David fixed his bike. He took it for a ride.",
         "output": "David fixed David's bike. David took the bike for a ride."},
         
        {"input": "Alice and Bob baked cookies. They shared them with their neighbors.",
         "output": "Alice and Bob baked cookies. Alice and Bob shared the cookies with Alice and Bob's neighbors."},
         
        {"input": "Emma read a book. She really enjoyed it.",
         "output": "Emma read a book. Emma really enjoyed the book."},
         
        {"input": "John and Michael cleaned their room. They found their lost toys.",
         "output": "John and Michael cleaned John and Michael's room. John and Michael found John and Michael's lost toys."},
        {"input": "John and Mary decided to go for a hike. She packed the snacks.",
         "output": "John and Mary decided to go for a hike. Mary packed the snacks."},
         
        {"input": "Alice noticed her cat was missing. She searched for it everywhere.",
         "output": "Alice noticed Alice's cat was missing. Alice searched for the cat everywhere."},
         
        {"input": "Michael and Sarah organized a party. They sent out the invitations.",
         "output": "Michael and Sarah organized a party. Michael and Sarah sent out the invitations."},
         
        {"input": "David was late for his meeting. He apologized to his boss.",
         "output": "David was late for David's meeting. David apologized to David's boss."},
         
        {"input": "Sophia baked a cake for her friend's birthday. She decorated it beautifully.",
         "output": "Sophia baked a cake for Sophia's friend's birthday. Sophia decorated the cake beautifully."},
         
        {"input": "Bob and Emma went to the zoo. They saw a lion there.",
         "output": "Bob and Emma went to the zoo. Bob and Emma saw a lion there."},
         
        {"input": "John lent his car to Michael. He promised to return it by evening.",
         "output": "John lent John's car to Michael. Michael promised to return the car by evening."},
         
        {"input": "Sarah and Alice played chess. She won the game.",
         "output": "Sarah and Alice played chess. Alice won the game."},
         
        {"input": "David's team worked late into the night. They were determined to finish the project.",
         "output": "David's team worked late into the night. David's team was determined to finish the project."},
         
        {"input": "Sophia saw her neighbor struggling with groceries. She offered to help him.",
         "output": "Sophia saw Sophia's neighbor struggling with groceries. Sophia offered to help the neighbor."},
         
        {"input": "Emma and Bob discussed their vacation plans. They decided to visit the mountains.",
         "output": "Emma and Bob discussed Emma and Bob's vacation plans. Emma and Bob decided to visit the mountains."},
         
        {"input": "John brought his guitar to the party. He played a few songs for everyone.",
         "output": "John brought John's guitar to the party. John played a few songs for everyone."},
         
        {"input": "Alice found her old diary. She read through it with nostalgia.",
         "output": "Alice found Alice's old diary. Alice read through the diary with nostalgia."},
         
        {"input": "Michael's family went on a road trip. They visited several national parks.",
         "output": "Michael's family went on a road trip. Michael's family visited several national parks."},
         
        {"input": "David fixed the leaking faucet in his kitchen. He felt proud of his work.",
         "output": "David fixed the leaking faucet in David's kitchen. David felt proud of David's work."},
         
        {"input": "Sophia wrote a letter to her grandmother. She told her all about her new job.",
         "output": "Sophia wrote a letter to Sophia's grandmother. Sophia told her grandmother all about Sophia's new job."},
         
        {"input": "John and Sarah planted flowers in their garden. They watered them every day.",
         "output": "John and Sarah planted flowers in John and Sarah's garden. John and Sarah watered the flowers every day."},
         
        {"input": "Alice borrowed a book from Emma. She promised to return it next week.",
         "output": "Alice borrowed a book from Emma. Alice promised to return the book next week."},
         
        {"input": "Bob's dog ran away from home. He searched the neighborhood until he found it.",
         "output": "Bob's dog ran away from home. Bob searched the neighborhood until Bob found the dog."},
         
        {"input": "Emma and Michael planned a surprise party for Sarah. They kept it a secret until the last moment.",
         "output": "Emma and Michael planned a surprise party for Sarah. Emma and Michael kept the party a secret until the last moment."},
         
        {"input": "David's company launched a new product. He was responsible for marketing it.",
         "output": "David's company launched a new product. David was responsible for marketing the product."},
         
        {"input": "Sophia and John attended a concert together. They enjoyed the music a lot.",
         "output": "Sophia and John attended a concert together. Sophia and John enjoyed the music a lot."},
         
        {"input": "Michael gave his sister a ride to the airport. She thanked him for his help.",
         "output": "Michael gave Michael's sister a ride to the airport. Michael's sister thanked Michael for Michael's help."},
         
        {"input": "Alice forgot to bring her umbrella. She got soaked in the rain.",
         "output": "Alice forgot to bring Alice's umbrella. Alice got soaked in the rain."},
         
        {"input": "Bob and Emma worked on their science project. They presented it to the class.",
         "output": "Bob and Emma worked on Bob and Emma's science project. Bob and Emma presented the project to the class."},
         
        {"input": "John's car broke down on the highway. He called a tow truck.",
         "output": "John's car broke down on the highway. John called a tow truck."},
         
        {"input": "Sophia and Alice went shopping. They bought new clothes for the summer.",
         "output": "Sophia and Alice went shopping. Sophia and Alice bought new clothes for the summer."},
         
        {"input": "Michael's dog chased a squirrel in the park. He laughed as it ran around.",
         "output": "Michael's dog chased a squirrel in the park. Michael laughed as the dog ran around."},
         
        {"input": "Emma and Sarah studied together for the exam. They were confident about their preparation.",
         "output": "Emma and Sarah studied together for the exam. Emma and Sarah were confident about Emma and Sarah's preparation."},
         
        {"input": "David brought his lunch to work. He shared it with his colleagues.",
         "output": "David brought David's lunch to work. David shared the lunch with David's colleagues."},
         
        {"input": "Sophia found a kitten near her house. She decided to adopt it.",
         "output": "Sophia found a kitten near Sophia's house. Sophia decided to adopt the kitten."},
         
        {"input": "John and Michael watched a movie together. They discussed it afterward.",
         "output": "John and Michael watched a movie together. John and Michael discussed the movie afterward."},
         
        {"input": "Alice and Bob went for a run in the morning. They felt energized afterward.",
         "output": "Alice and Bob went for a run in the morning. Alice and Bob felt energized afterward."},
         
        {"input": "Emma's mother cooked dinner. She made her favorite dish.",
         "output": "Emma's mother cooked dinner. Emma's mother made Emma's favorite dish."},
         
        {"input": "David and Sarah cleaned their house on the weekend. They worked together to get it done quickly.",
         "output": "David and Sarah cleaned David and Sarah's house on the weekend. David and Sarah worked together to get the house cleaned quickly."},
         
        {"input": "Sophia's friend invited her to a party. She was excited to attend.",
         "output": "Sophia's friend invited Sophia to a party. Sophia was excited to attend the party."},
         
        {"input": "John and Alice planned a vacation. They booked their flights early.",
         "output": "John and Alice planned a vacation. John and Alice booked John and Alice's flights early."},
         
        {"input": "Michael forgot his keys at home. He had to wait outside until someone arrived.",
         "output": "Michael forgot Michael's keys at home. Michael had to wait outside until someone arrived."},
         
        {"input": "Sarah and Emma attended a workshop. They learned new skills.",
         "output": "Sarah and Emma attended a workshop. Sarah and Emma learned new skills."},
         
        {"input": "David and Bob played tennis. They enjoyed their match.",
         "output": "David and Bob played tennis. David and Bob enjoyed their match."},
         
        {"input": "Sophia's sister borrowed her dress. She returned it after the weekend.",
         "output": "Sophia's sister borrowed Sophia's dress. Sophia's sister returned the dress after the weekend."}
    ]


    from ollama import OllamaModel, OllamaTrainer

    # Load base model
    model = OllamaModel.load_pretrained("gpt-3")


    # Fine-tune the model
    trainer = OllamaTrainer(model=model, dataset=dataset, task="pronoun_resolution")
    trainer.train(epochs=5, batch_size=32)

    # Save the fine-tuned model
    model.save("pronoun_resolution_model")

    # Test the model
    test_input = "Alice met John at the park. He was late."
    result = model.predict(test_input)
    print(result)  # Expected: "Alice met John at the park. John was late."

    return (
        OllamaModel,
        OllamaTrainer,
        dataset,
        model,
        result,
        test_input,
        trainer,
    )


if __name__ == "__main__":
    app.run()
