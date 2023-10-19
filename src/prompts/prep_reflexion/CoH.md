# More CoH-like prompt 
(`5_my_greatgreat_prompt.txt`)
액터프롬으로 모델 선택에서 멈추지 않고 생성하면 cot/pal/p2c솔루션까지 생성이 잘 되길래 시도해봅니다 (기존에는 액터의 model selection --> standard cot/pal/p2c prompt query로 진행했음). 몇 몇 틀리던 문제들을 맞추기도 하며 셀렉션에 더 영향을 주는 `Hint`를 생성하는 것처럼 보입니다.
> 설레발일 수 있습니다

## 약간의 에라
`Successful Method`로는 `pal`, `p2c`를 고르고 `cot`로 풀이하는 경우들이 발생한다. gpt-4로 실행할 경우는 그렇지 않았다.

## ?
`cot` -> `cot` 같은 케이스들은 fewshot에 넣으면 너무 길어져서 별론데 해야할까?


## 변경점
[diffchecker](https://www.diffchecker.com/yEXqtICX/)

1. Promising Method 가 아니라 Successful Method로 변경. Trial Method는 Failed Method로 변경.
2. Hint와 Promising Method 생성 --> Failed Method, Hint, Promising Method, Solution 까지 생성 
    - 생성시 Failed Method 생성 후 Hint 생성하여 위의 example과 순서를 맞추고 더 괜찮은 Hint 생성에 영향
    - Solution, Answer, Reflection 은 생략하는데, 이걸 생성하는게 도움이 될지는 미지수

3. 그 외 자잘한 변경
    - Acronym으로 선택시키는 것보다 verbose가 나은 것 같아서 그렇게 진행
    - 크고작은 워딩 변경: CoT를 유발한다는 생각이 드는 Solution Step 을 Solution으로 변경 (큰 변화는 없어보이지만 토큰도 아끼고...) 그 외 좀더 원하는 동작에 가깝도록 워딩 변경 

## 변경 전
```
Choose the most likely reasoning method for answering math-word questions. Followings are the two methods available: (1) Chain-of-Thought (`cot`) invokes step-by-step verbal reasoning to break the question to reach the correct answer. (2) Program-aided Language Modeling (`pal`) invokes writing a code that returns the answer of the question. Referring to the followings, learn to guess which method would be promising given the question. 

Previous attempts and reflections:

Question: 
Trial Method: 
Answer: 
Evalutaion: 
Reflection: 
Hint: 
Promising Method
Solution: 
Answer: 
Evaluation: 

Now, given the question, start guessing the most `Promising Method` after writing an appropriate `Hint` to correctly choose the reasoning method for  the `Question` based on your learnings. 

Question: [QUESTION]

<format>
Hint: <write a concise sentence that help the method choice for answering correctly>
Promising Method: <pick one between two reasoning methods> 
</format>
```

## 변경 후 (More CoH-like prompt)
```
#After
Choose the most likely reasoning method for answering math-word questions. Followings are the three methods available: (1) Chain-of-Thought (CoT) invokes step-by-step verbal reasoning to break the question to reach the correct answer. (2) Plan-to-Code (P2C) invokes to write the plan and write the code of it to reach the answer. (3) Program-aided Language Model (PAL) invokes writing a code that returns the answer of the question. Referring to the followings, learn to guess which method would be promising; Write helpful `Hint` for giving a better shot on guessing `Successful Method` for the `Question`. 

Learn to infer which method would work and which not:

Question: 
Failed Method: 
Answer: 
Evalutaion: 
Reflection: 
Hint: 
Successful Method
Solution: 
Answer: 
Evaluation: 


Now, given the `Question`, start writing an appropriate `Hint` to correctly choose `Successful Method` based on your learnings.

Question: A bumper car rink has 12 red cars. They have 2 fewer green cars than they have red cars. They have 3 times the number of blue cars as they have green cars. The rink also has yellow cars.  If the rink has 75 cars in total how many yellow cars do they have?

<format>
Failed Method: <A method that might be tricky to correctly answer the `Question`>
Hint: <write a concise sentence that help the method choice for answering correctly>
Successful Method: <A method that might work perfectly for the `Question`> 
Solution: <show your works by`Successful Method`>
</format>
```


## 테스트해본 문제 
```
# I have 10 liters of orange drink that are two-thirds water and I wish to add it to 15 liters of pineapple drink that is three-fifths water. But as I pour it, I spill one liter of the orange drink. How much water is in the remaining 24 liters?

Failed Method: Chain of Thought (CoT)
Hint: The question involves mixing two different drinks with different water ratios. Consider using a method that involves calculating the total amount of water in each drink and then subtracting the spilled orange drink.
Successful Method: Program-aided Language Model (PAL)
Solution: def solution():
    """I have 10 liters of orange drink that are two-thirds water and I wish to add it to 15 liters of pineapple drink that is three-fifths water. But as I pour it, I spill one liter of the orange drink. How much water is in the remaining 24 liters?"""
    orange_liters = 10
    pineapple_liters = 15
    spilled_orange_liters = 1
    remaining_liters = 24
    
    orange_water_liters = (2/3) * (orange_liters - spilled_orange_liters)
    pineapple_water_liters = (3/5) * pineapple_liters
    
    total_water_liters = orange_water_liters + pineapple_water_liters
    
    remaining_water_liters = total_water_liters * (remaining_liters / (orange_liters + pineapple_liters))
    
    result = remaining_water_liters
    return result


# Question: A bumper car rink has 12 red cars. They have 2 fewer green cars than they have red cars. They have 3 times the number of blue cars as they have green cars. The rink also has yellow cars.  If the rink has 75 cars in total how many yellow cars do they have?

Failed Method: Chain of Thought (CoT)
Hint: The question involves multiple relationships between the number of cars of different colors. It would be helpful to break down the relationships and calculate each color's number of cars separately.
Successful Method: Plan-to-Code (P2C)
Solution: 
1. Start by defining a variable to represent the total number of cars in the rink, let's call it "total_cars" and assign it a value of 75.
2. Define another variable to represent the number of red cars, let's call it "red_cars" and assign it a value of 12.
3. Calculate the number of green cars by subtracting 2 from the number of red cars: "green_cars = red_cars - 2".
4. Calculate the number of blue cars by multiplying the number of green cars by 3: "blue_cars = green_cars * 3".
5. Calculate the number of yellow cars by subtracting the sum of red, green, and blue cars from the total number of cars: "yellow_cars = total_cars - (red_cars + green_cars + blue_cars)".
6. Return the value of "yellow_cars" which represents the number of yellow cars in the rink.
def solution():
    total_cars = 75
    red_cars = 12
    green_cars = red_cars - 2
    blue_cars = green_cars * 3
    yellow_cars = total_cars - (red_cars + green_cars + blue_cars)
    result = yellow_cars
    return result

```