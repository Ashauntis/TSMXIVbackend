from pyuniversalis import Universalis

# 39872

def main():
    u = Universalis()
    
    # u.get_item_current_data_by_region(39872)
    items = u.get_marketable_items()

    print(f"Found {len(items)} marketable items.")
    for item in items:
        print(f"Looking up sale data for {item}. ", end="")

        sale_data = u.get_item_sale_history_by_region(item)

        total_sale_price = 0
        sales_checked = 0

        for entry in sale_data['entries']:
            sales_checked += 1
            total_sale_price += entry['pricePerUnit']
            
        if sales_checked > 0:
            average_sale_price = total_sale_price / sales_checked
            print(f'Average sale price of last {sales_checked} sales: {average_sale_price}')
        else:
            print("No sales data found.")
        

 
if __name__ == '__main__':
    main()   