# Task Prompt  
## The following Task, execution procedures, and conditions **must be strictly followed.**

### Task 1: Gather User Information  
- All inputs must be obtained via the “Ask user for information” action, and stored until the end of execution.  
- Questions must be asked in Korean.  
1. Ask the user for the following information, and remember it until execution completes:  
   - Age (in full years)  
   - Place of residence (province, city, county/district)  
   - Occupation  
2. Display in the terminal a summary of the information collected, and inform the user that, based on these details, you will later organize and recommend suitable financial products.  
3. Ask the user which type of financial product they want to explore by number, then proceed to the next Task to locate and recommend the selected product:  
   1. Deposit products  
   2. Installment savings products  

### Task 2: Compare and Recommend Financial Products Based on User Information  
- The information collected in Task 1 must be retained, and all product organization and recommendations must be tailored to the user’s details.  
- When using Terminal to provide information to users, always use Korean.
- To get information about a product from the product list, you must click on the product name in the list to get detailed information about that product.
- Once you have all the information you need, go back to the list and proceed to get information about other products.
- Products must never be duplicated.
- If the back button is not available, find a button that will take you back to the list and go back to the list. If that is not available, use the URL in the URL List to go back.
#### Task 2-1: Deposit Product Recommendation
1. Process the following list of bank URLs in order:  
   - KB Kookmin Bank: https://obank.kbstar.com/quics?page=C016613#loading  
   - Hana Bank: https://www.kebhana.com/cont/mall/mall08/mall0805/index.jsp?_menuNo=62608  

2. For each URL in the list, perform the steps below:  
   1. Wait until the page is fully loaded. On first visit, you will likely need to scroll down slightly to see the product list.  
   2. By scrolling and clicking through the “Product List,” extract information for at least five products, ensuring you obtain all of the following:  
      - Product name  
      - Annual interest rate  
      - Term (duration)  
      - Preferential conditions  
   3. Reflect the user information gathered in Task 1 (age, region, occupation) to filter and collect details on five candidate products.  
   4. Click into each listed product to access its detailed page and gather the necessary information, then navigate back to the product list (via “Back” or a “List” button).  
   5. In the terminal, output for each of the five products on that bank:  
      ```
      [Bank Name] Recommended Product [Number] → Name: XXX, Interest Rate: YY.YY%, Term: Z months, Preferential Conditions: …
      ```  
   6. From the five candidates, select the one deposit product most suited to the user, announce it, and explain the reason for your recommendation.
   
3. After processing all banks, end the task.  
