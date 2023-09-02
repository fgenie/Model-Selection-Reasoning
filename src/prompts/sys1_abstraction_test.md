System message:
You are tutoring a student who wants to learn python. You are great at teaching how to break down solving math word problems with step-by-step plans in number list so that your student actually code an appropriate solution by following it.

User:
Followings are math word problems to be covered. You will give numbered steps about how to reach to the answer of the questions. For example, consider the math problem below. 

Question: Olivia has $23. She bought five bagels for $3 each. How much money does she have left?

Suggestion:
1. Check how much money Olivia had at first, and store it into some variable.
2. She's consuming it to buy bagels. You can subtract the cost of bagel multiplied by number of bagels to figure out how much did she consume.
3. Subtract the cost from initial deposit.
4. Return the calculated number.
</end>

Now let's start this for following questions. Your answer will start with "Suggestion:" and end with `</end>` tag after you are all done.
Question: There were nine computers in the server room. Five more computers were installed each day, from monday to thursday. How many computers are now in the server room?

Assistant: Suggestion:
1. Start with the initial number of computers in the server room, which is nine. Store this number in a variable.
2. From Monday to Thursday, five more computers were installed each day.
3. Add five computers to the initial number for each day from Monday to Thursday. This means adding five four times.
4. Keep track of the running total by updating the variable that stores the number of computers.
5. Return the final number of computers in the server room.
</end>


Question: Find the prime number that is larger than 11.
1. Start with the number 12.
2. Check if the number is divisible by any number smaller than itself (excluding 1).
3. If it is divisible by any number, increment the number by 1 and repeat step 2.
4. If the number is not divisible by any number, it is a prime number.
5. Return the prime number.
</end>

If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23. Find the sum of all the multiples of 3 or 5 below 1000.
1. Initialize a variable called "sum" with a value of 0 to keep track of the sum of the multiples.
2. Use a loop to iterate through all the natural numbers below 1000.
3. Within the loop, use an if statement to check if the current number is a multiple of 3 or 5.
4. If the current number is a multiple of 3 or 5, add it to the "sum" variable.
5. After the loop, print or return the value of the "sum" variable.

</end>

235*12=?

1. Create a variable to store the first number, 235.
2. Create a variable to store the second number, 12.
3. Multiply the two numbers together using the * operator.
4. Store the result in a new variable.
5. Return the calculated result.
</end>





Followings are math word problems to be covered. You will give numbered steps about how to reach to the answer of the questions. For example, consider the math problem below. 

Question: Olivia has $23. She bought five bagels for $3 each. How much money does she have left?

Suggestion:
1. Check how much money Olivia had at first, and store it into some variable.
2. She's consuming it to buy bagels. You can subtract the cost of bagel multiplied by number of bagels to figure out how much did she consume.
3. Subtract the cost from initial deposit.
4. Return the calculated number.
</end>

Question: Find the prime number that is larger than 11.

1. Start by initializing a variable to store the current number and set it to 12.
2. Create a loop that will keep running until a prime number is found. 
3. Inside the loop, check if the current number is prime or not. 
4. Implement a function to check primality. A common way is to iterate from 2 to the square root of the current number and check if any number divides it evenly. If a divisor is found, the number is not prime. 
5. If the current number is prime, break out of the loop. 
6. Otherwise, increment the current number by 1 and continue to the next iteration of the loop. 
7. After the loop ends, return the prime number that was found.
</end>

Now let's start this for following questions. Your answer will start with "Suggestion:" and end with `</end>` tag after you are all done. Note that the last step of the suggestion need to clearly state returning the answer of the question.
Question: If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23. Find the sum of all the multiples of 3 or 5 below 1000.

1. Start by initializing a variable named `sum` to store the sum of multiples and set it to 0.
2. Create a loop that will iterate through each number from 1 to 999 (since we want multiples below 1000).
3. Inside the loop, check if the current number is divisible by either 3 or 5 using a condition statement (e.g., if the current number modulo 3 is 0 or the current number modulo 5 is 0).
4. If the current number is divisible by either 3 or 5, add it to the `sum` variable.
5. After the loop ends, return the value of the `sum` variable as the sum of the multiples of 3 or 5 below 1000.

</end>