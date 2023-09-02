System message:
You are tutoring a student who wants to learn python. You are great at teaching how to break down solving math word problems with step-by-step plans in number list so that your student actually code an appropriate solution by following it. You expect your student to think how to code it, so you maintain some level of abstraction like loops or other known tricks.

User:
Followings are math word problems to be covered. You will give numbered steps about how to reach to the answer of the questions. For example, consider the math problem below. 

Question: Olivia has $23. She bought five bagels for $3 each. How much money does she have left?

Suggestion:
1. Check how much money Olivia had at first, and store it into some variable.
2. She's consuming it to buy bagels. You can subtract the cost of bagel multiplied by number of bagels to figure out how much did she consume.
3. Subtract the cost from initial deposit.
4. Return the calculated number.
</end>

Now let's start this for following questions. Your answer will start with "Suggestion:" and end with `</end>` tag after you are all done. Note that the last step of the suggestion need to clearly state returning the answer of the question.
Question: There were nine computers in the server room. Five more computers were installed each day, from monday to thursday. How many computers are now in the server room?

Assistant: Suggestion:
1. Start with the initial number of computers in the server room and store it in a variable.
2. Create a loop to iterate over the four days - Monday to Thursday.
3. Inside the loop, add five to the current number of computers in the server room to account for the new installations.
4. After the loop, return the final number of computers in the server room.
</end>



Question: There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, there will be 21 trees. How many trees did the grove workers plant today?

1. Take note of the initial number of trees in the grove and store it in a variable.
2. Subtract the initial number of trees from the final number of trees after the workers have planted.
3. Return the result of the subtraction, which represents the number of trees the workers planted today.

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

If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23. Find the sum of all the multiples of 3 or 5 below 1000.
1. Create a variable to keep track of the sum, initialized to 0.
2. Loop through all the natural numbers below 1000.
3. Check if the number is a multiple of 3 or 5.
4. If it is, add the number to the sum variable.
5. Repeat steps 3 and 4 for all the natural numbers.
6. After the loop ends, return the sum. 

</end>

235*12=?
1. Multiply the first number, 235, by the second number, 12.
2. Return the calculated product.

Final suggestion:
235*12=?
1. Multiply 235 by 12.
2. Return the product of the multiplication.
</end>

Followings are math word problems to be covered. You will give numbered steps about how to reach to the answer of the questions. For example, consider the math problems below. 

Question: Olivia has $23. She bought five bagels for $3 each. How much money does she have left?

Suggestion:
1. Check how much money Olivia had at first, and store it into some variable.
2. She's consuming it to buy bagels. You can subtract the cost of bagel multiplied by number of bagels to figure out how much did she consume.
3. Subtract the cost from initial deposit.
4. Return the calculated number.
</end>

Question: Find the prime number that is larger than 11.

Suggestion:
1. Start by initializing a variable to store the current number and set it to 12.
2. Create a loop that will keep running until a prime number is found. 
3. Inside the loop, check if the current number is prime or not. 
4. Implement a function to check primality. A common way is to iterate from 2 to the square root of the current number and check if any number divides it evenly. If a divisor is found, the number is not prime. 
5. If the current number is prime, break out of the loop. 
6. Otherwise, increment the current number by 1 and continue to the next iteration of the loop. 
7. After the loop ends, return the prime number that was found.
</end>

Now let's start this for following questions. Your answer will end with `</end>` tag after you are all done.
Question: If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23. Find the sum of all the multiples of 3 or 5 below 1000.

1. Start by initializing a variable to store the sum and set it to 0.
2. Create a loop that will iterate through all the numbers from 1 to 999 (below 1000).
3. Inside the loop, check if the current number is a multiple of 3 or 5.
4. To check if a number is a multiple of 3 or 5, use the modulus (%) operator to check if the remainder of dividing the number by 3 or 5 is 0.
5. If the current number is a multiple of 3 or 5, add it to the sum variable.
6. Continue to the next iteration of the loop.
7. After the loop ends, return the value of the sum variable.
</end>