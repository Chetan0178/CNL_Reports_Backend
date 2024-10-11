from decimal import Decimal
from django.db import connection
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from report_proj.myapp.models import ReportDefinition
from report_proj.myapp.serializers import ReportDefinitionSerializer
import json
from collections import defaultdict

class reports(APIView):
    def get(self, request, **kwargs):
        try:
            report = ReportDefinition.objects.get(name=kwargs.get('query_name'))
            serializer = ReportDefinitionSerializer(report).data
            with connection.cursor() as cursor:
                query = serializer.get('query')
                cursor.execute(query)
                results = cursor.fetchall()

            if 'monthly-sales' == kwargs.get('query_name'):
                #Prepare the response data
                months = [
                    "January", "February", "March", "April", "May", 
                    "June", "July", "August", "September", "October", 
                    "November", "December"
                ]
                sales_count = [0] * 12

                for result in results:
                    month_index = int(result[0]) - 1
                    sales_count[month_index] = result[1]

                response_data = {
                    "month": months,
                    "sales_count": sales_count,
                }
            
            elif 'sales-order-trend-daily' == kwargs.get('query_name'):
                # Initialize the lists
                dates = []
                order_count = []
                invoices = []
                returns = []

                # Iterate through the data and populate the lists
                for entry in results:
                    dates.append(entry[0])         # Date is the first element
                    order_count.append(entry[1])   # Order count is the second element
                    invoices.append(entry[2])      # Invoices count is the third element
                    returns.append(entry[3])       # Returns count is the fourth element

                # Create the final output dictionary   
                response_data = {
                    "dates": dates,
                    "order_count": order_count,
                    "invoices": invoices,
                    "returns": returns
                }
                
            elif 'sales-order-trend-weekly' == kwargs.get('query_name'):
                # # Initialize the lists
                # # Initialize lists for the weeks
                # first_week = []
                # second_week = []
                # third_week = []
                # fourth_week = []
                # order_count = []
                # invoices = []
                # returns = []
                #   # Print the results


                # # Iterate through the data and populate the lists
                # for entry in results:
                #     year, week_number, _, _, _ = entry
                #     if week_number % 4 == 1:  # 1st week of the month
                #         first_week.append(week_number)
                #     elif week_number % 4 == 2:  # 2nd week of the month
                #         second_week.append(week_number)
                #     elif week_number % 4 == 3:  # 3rd week of the month
                #         third_week.append(week_number)
                #     elif week_number % 4 == 0:  # 4th week of the month
                #         fourth_week.append(week_number)
                #     order_count.append(entry[2])   # Order count is the second element
                #     invoices.append(entry[3])      # Invoices count is the third element
                #     returns.append(entry[4])       # Returns count is the fourth element

                # week = {'first_week' : first_week,
                #         'second_week' : second_week,
                #         'third_week' : third_week,
                #         'fourth_week' : fourth_week
                #     }
                
                weeks = []
                order_count = []
                invoices = []
                returns = []

                # Populate the lists
                for entry in results:
                    weeks.append(entry[1])  # Week number
                    order_count.append(entry[2])      # Total Sales Orders
                    invoices.append(entry[3])      # Converted To Invoices
                    returns.append(entry[4]) 

                # Create the final output dictionary   sales-order-trend-weekly
                response_data = {
                    "dates": weeks,
                    "order_count": order_count,
                    "invoices": invoices,
                    "returns": returns
                }
            
            elif 'sales-order-trend-monthly' == kwargs.get('query_name'):
                # Initialize the lists
                Week_Number = []
                order_count = []
                invoices = []
                returns = []

                
                # Iterate through the data and populate the lists
                for entry in results:
                    Week_Number.append(entry[1])         # Date is the first element
                    order_count.append(entry[2])   # Order count is the second element
                    invoices.append(entry[3])      # Invoices count is the third element
                    returns.append(entry[4])       # Returns count is the fourth element

                # Create the final output dictionary   sales-order-trend-weekly
                response_data = {
                    "dates": Week_Number,
                    "order_count": order_count,
                    "invoices": invoices,
                    "returns": returns
                }
            
            elif 'Sales-Performance-by-Customer' == kwargs.get('query_name'):
                # Organize data by customer names and product categories
                customers = set()
                categories = set()
                sales_data = defaultdict(lambda: defaultdict(float))

                for customer, category, sales in results:
                    customers.add(customer)
                    categories.add(category)
                    sales_data[customer][category] = float(sales)  # Ensure sales are float

                # Sort customers and categories for consistent labeling
                sorted_customers = sorted(customers)
                sorted_categories = sorted(categories)

                # Prepare separate lists
                cust_name_list = sorted_customers
                prod_category_list = sorted_categories
                price_list = [[sales_data[customer].get(category, 0.0) for customer in sorted_customers] for category in sorted_categories]

                # Combine into a dictionary for the API response
                response_data = {
                    "cust_name_list": cust_name_list,
                    "prod_category_list": prod_category_list,
                    "price_list": price_list
                }


            # elif 'top-1-high-selling-Products-monthly' == kwargs.get('query_name'):
            #     # Define the order of months
            #     month_order = [
            #         "January", "February", "March", "April", "May", 
            #         "June", "July", "August", "September", "October", 
            #         "November", "December"
            #     ]

            #     # Initialize dictionaries to hold data
            #     months = []
            #     product_names = []
            #     sales_dict = {}

            #     # Populate sales data
            #     for entry in results:
            #         month, product, sales = entry
            #         months.append(month)
            #         product_names.append(product)
                    
            #         if product not in sales_dict:
            #             sales_dict[product] = {month: sales}
            #         else:
            #             if month not in sales_dict[product]:
            #                 sales_dict[product][month] = sales
            #             else:
            #                 sales_dict[product][month] += sales  # Aggregate sales for same product and month

            #     # Prepare the final sales list
            #     sales = []

            #     for product in sales_dict:
            #         sales_list = []
            #         for month in month_order:
            #             sales_list.append(sales_dict[product].get(month, 0))
            #         sales.append(sales_list)

            #     # Print the final lists
            #     response_data = {
            #         "months": months,
            #         "product_names": product_names,
            #         "sales": sales
            #     }
            elif 'High-Selling-Products-monthly' == kwargs.get('query_name'):
                # Initialize lists
                months = [
                    "January", "February", "March", "April", "May", "June", 
                    "July", "August", "September", "October", "November", "December"
                ]

                product_names = set()
                sales_data = {month: [] for month in months}

                # Process the data
                for month, product, sales in results:
                    if product not in product_names:
                        product_names.add(product)
                    
                    sales_data[month].append((product, sales))

                # Create a sorted list of product names
                product_names = sorted(product_names)

                # Initialize sales list
                sales = [[] for _ in range(len(product_names))]

                # Fill in sales data
                for month in months:
                    for product in product_names:
                        # Find the sales amount for the current product in the current month
                        amount = next((sale for prod, sale in sales_data[month] if prod == product), 0)
                        # Append the sales amount to the corresponding product's sales list
                        sales[product_names.index(product)].append(amount)

                # Output
                response_data = {
                    "label": months,
                    "product_names": product_names,
                    "sales_data": sales
                    }  

            elif 'High-Selling-Products-weekly' == kwargs.get('query_name'):
                # Initialize lists
                # Initialize lists
                week = []
                product_names = []
                sales_data = {}

                # Process the data
                for week_number, product, sales in results:
                    if week_number not in week:
                        week.append(week_number)
                    
                    if product not in product_names:
                        product_names.append(product)
                        sales_data[product] = [0] * len(week)  # Initialize sales data for the new product
                    
                    week_index = week.index(week_number)
                    
                    # Ensure the index is within the range
                    if week_index < len(sales_data[product]):
                        sales_data[product][week_index] += sales
                    else:
                        # Handle case where week_index exceeds current sales_data size
                        sales_data[product].extend([0] * (week_index - len(sales_data[product]) + 1))
                        sales_data[product][week_index] += sales

                # Convert sales_data from dict to list format
                sales_data_list = [sales_data[product] for product in product_names]

                # Output
                response_data = {
                    "label": week,
                    "product_names": product_names,
                    "sales_data": sales_data_list
                } 

            elif 'High-Selling-Products-yearly' == kwargs.get('query_name'):
                # Initialize the output structure
                years = []
                product_names = []
                sales_data = {}

                # Process the data
                for entry in results:
                    year, product, sales = entry
                    
                    # Ensure the year is in the list
                    if year not in years:
                        years.append(year)
                    
                    # Initialize product in the sales_data if not already present
                    if product not in product_names:
                        product_names.append(product)
                        sales_data[product] = [0] * len(years)  # Create a sales list initialized to 0 for each year

                    # Find the index of the current year
                    year_index = years.index(year)
                    
                    # Ensure the sales_data for the product has the correct length
                    while len(sales_data[product]) < len(years):
                        sales_data[product].append(0)  # Fill with zeros if necessary

                    sales_data[product][year_index] += sales  # Accumulate sales

                # Prepare the final output

                # Final output structure
                response_data = {
                    "label": years,
                    "product_names": product_names,
                    "sales_data": [sales_data[product] for product in product_names],
                }


            elif 'todays_revenue' == kwargs.get('query_name'):
                # Extracting the revenue
                revenue = results[0][0]

                # Creating the desired dictionary
                response_data = {
                    "label": "todays_revenue",
                    "revenue": revenue
                }
                
            elif 'yesterday_revenue' == kwargs.get('query_name'):
                # Extracting the revenue
                revenue = results[0][0]

                # Creating the desired dictionary
                response_data = {
                    "label": "yesterday_revenue",
                    "revenue": revenue
                }    

            elif 'last_3_months_revenue' == kwargs.get('query_name'):
                # Initialize the lists
                months = []
                revenue = []

                # Extracting the data
                for item in results:
                    months.append(item[0])  # Append the month
                    revenue.append(item[1])  # Append the revenue
                
                response_data = {
                    "label": months,
                    "revenue": revenue
                } 
                
            elif 'last_7_days_revenue' == kwargs.get('query_name'):
                # Extracting the revenue
                revenue = results[0][0]

                # Creating the desired dictionary
                response_data = {
                    "label": "last_7_days_revenue",
                    "revenue": revenue
                }  

            elif 'current_month_revenue' == kwargs.get('query_name'):
                # Extracting the revenue
                label = results[0][0]
                revenue = results[0][1]

                # Creating the desired dictionary
                response_data = {
                    "label": label,
                    "revenue": revenue 
                } 
            elif 'last_month_revenue' == kwargs.get('query_name'):   
                # Extracting the revenue
                label = results[0][0]
                revenue = results[0][1]

                # Creating the desired dictionary
                response_data = {
                    "label": label,
                    "revenue": revenue  
                } 
        
            elif 'last_6_month_revenue' == kwargs.get('query_name'):
                # Initialize the lists
                months = []
                revenue = []

                # Extracting the data
                for item in results:
                    months.append(item[0])  # Append the month
                    revenue.append(item[1])  # Append the revenue
                
                response_data = {
                    "label": months,
                    "revenue": revenue
                } 

            elif 'current_quarter_revenue' == kwargs.get('query_name'):   
                # Initialize the lists
                months = []
                revenue = []

                # Extracting the data
                for item in results:
                    months.append(item[0])  # Append the month
                    revenue.append(item[1])  # Append the revenue
                
                response_data = {
                    "label": months,
                    "revenue": revenue
                } 
            
            elif 'year_to_date' == kwargs.get('query_name'):   
                # Initialize the lists
                months = []
                revenue = []

                # Extracting the data
                for item in results:
                    months.append(item[0])  # Append the month
                    revenue.append(item[1])  # Append the revenue
                
                response_data = {
                    "label": months,
                    "revenue": revenue
                } 
            
            elif 'year_to_last_month' == kwargs.get('query_name'):    
                # Extracting the revenue
                revenue = results[0][0]

                # Creating the desired dictionary
                response_data = {
                    "label": "Last Year",
                    "revenue": revenue  
                } 
                pass

            return Response(response_data, status=status.HTTP_200_OK) 
        except ReportDefinition.DoesNotExist:
            return Response({"error": "Report not found."}, status=status.HTTP_404_NOT_FOUND)

        

