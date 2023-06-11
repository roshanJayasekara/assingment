import streamlit as st
import pandas as pd

# Sample mobile phone dataset
mobile_phones = [
    {
        'brand': 'Apple',
        'model': 'iPhone 12',
        'price': 999,
        'os': 'iOS',
        'display_size': 6.1,
        'camera': 12,
        'storage': 64,
        'battery': 2815
    },
    {
        'brand': 'Apple',
        'model': 'iPhone 13',
        'price': 1100,
        'os': 'iOS',
        'display_size': 6.1,
        'camera': 12,
        'storage': 128,
        'battery': 2815
    },
    {
        'brand': 'Apple',
        'model': 'iPhone 14',
        'price': 1300,
        'os': 'iOS',
        'display_size': 6.1,
        'camera': 12,
        'storage': 64,
        'battery': 2815
    },
    {
        'brand': 'Apple',
        'model': 'iPhone SE',
        'price': 399,
        'os': 'iOS',
        'display_size': 4.7,
        'camera': 12,
        'storage': 64,
        'battery': 1821
    },
    {
        'brand': 'Google',
        'model': 'Pixel 6',
        'price': 650,
        'os': 'Android',
        'display_size': 6.4,
        'camera': 50,
        'storage': 128,
        'battery': 4000
    },
    {
        'brand': 'Google',
        'model': 'Pixel 7',
        'price': 720,
        'os': 'Android',
        'display_size': 6.4,
        'camera': 50,
        'storage': 128,
        'battery': 4614
    },
    {
        'brand': 'Google',
        'model': 'Pixel 7 pro',
        'price': 820,
        'os': 'Android',
        'display_size': 6.7,
        'camera': 50,
        'storage': 256,
        'battery': 4500
    }, 
    
    {
        'brand': 'Motorola',
        'model': 'Moto G Power',
        'price': 249,
        'os': 'Android',
        'display_size': 6.6,
        'camera': 48,
        'storage': 64,
        'battery': 5000
    },
    {
        'brand': 'Samsung',
        'model': 'Galaxy S22',
        'price': 799,
        'os': 'Android',
        'display_size': 6.2,
        'camera': 12,
        'storage': 128,
        'battery': 4000
    },
    {
        'brand': 'Samsung',
        'model': 'Galaxy A52',
        'price': 450,
        'os': 'Android',
        'display_size': 6.5,
        'camera': 64,
        'storage': 128,
        'battery': 4500
    },
    {
        'brand': 'Oppo',
        'model': 'Find X3 Pro',
        'price': 1199,
        'os': 'Android',
        'display_size': 6.7,
        'camera': 50,
        'storage': 256,
        'battery': 4500
    },
    {
        'brand': 'Oppo',
        'model': 'Reno 6 Pro',
        'price': 699,
        'os': 'Android',
        'display_size': 6.5,
        'camera': 64,
        'storage': 128,
        'battery': 4500
    },
    {
        'brand': 'Xiaomi',
        'model': 'Mi 11 Ultra',
        'price': 1250,
        'os': 'Android',
        'display_size': 6.81,
        'camera': 50,
        'storage': 256,
        'battery': 5000
    },
    {
        'brand': 'Xiaomi',
        'model': 'Redmi Note 10 Pro',
        'price': 299,
        'os': 'Android',
        'display_size': 6.67,
        'camera': 108,
        'storage': 128,
        'battery': 5020
    },
    # Add more mobile phone data here...
]

# Conversion rate from USD to LKR (Sri Lankan Rupees)
conversion_rate = 296

# Function to recommend mobile phones based on user preferences
def recommend_mobile_phone(preferences):
    matching_phones = []
    for phone in mobile_phones:
        if phone['os'] == preferences['os']:
            if phone['display_size'] >= preferences['display_size']:
                if phone['camera'] >= preferences['camera']:
                    if phone['storage'] >= preferences['storage']:
                        if phone['battery'] >= preferences['battery']:
                            matching_phones.append(phone)
    return matching_phones

# Main Streamlit app
def main():
    st.title("Mobile Phone Recommender")

    # User preferences form
    budget = st.slider("Select your budget (in LKR):", min_value=10_000, max_value=500_000, step=1000, value=100_000)
    os = st.selectbox("Select your preferred operating system:", ['iOS', 'Android'])
    display_size = st.number_input("Enter your preferred display size (in inches):", value=6.0)
    camera = st.slider("Select your required camera quality (in megapixels):", min_value=1, max_value=50, step=1, value=10)
    storage = st.slider("Select your required storage capacity (in GB):", min_value=1, max_value=512, step=1, value=64)
    battery = st.slider("Select your required battery capacity (in mAh):", min_value=1000, max_value=10000, step=100, value=3000)

    preferences = {
        'budget': budget,
        'os': os,
        'display_size': display_size,
        'camera': camera,
        'storage': storage,
        'battery': battery
    }

    # Button to recommend mobile phones based on preferences
    if st.button("Recommend a Phone"):
        # Recommend mobile phones based on preferences
        recommendations = recommend_mobile_phone(preferences)

        # Display the recommended mobile phones
        if recommendations:
            diff_list=[]
            df = pd.DataFrame(columns=['Brand', 'Model',"Price(LKR)","Price Difference"])
            st.subheader("Recommended Mobile Phones:")
            for phone in recommendations:
                price_lkr = phone['price']*conversion_rate
                price_diff = abs(price_lkr - preferences['budget'])
                diff_list.append(price_diff)
                df = df.append({'Brand': phone['brand'],'Model':phone['model'], "Price(LKR)":price_lkr,"Price Difference":price_diff}, ignore_index=True)
                #st.write(f"Brand: {phone['brand']}, Model: {phone['model']}, Price: LKR {price_lkr}, Price Difference: LKR {price_diff}")
            column1_sum = df['Price Difference'].sum()
            df['Price Difference2'] = (1-df['Price Difference'] / column1_sum) * 100
            df['Price Difference2'] = df['Price Difference2'].replace(0, 100)
            column2_sum = df['Price Difference2'].sum()
            df['Recommendation Probability'] = (df['Price Difference2'] / column2_sum)
            sorted_df = df.sort_values(by='Recommendation Probability',ascending=False)
            sorted_df = sorted_df.drop(['Price Difference2',"Price Difference"], axis=1)
            st.write(sorted_df.head(4))
        else:
            st.subheader("Recommended Mobile Phones:")
            alternative_phones = []
            diff_list=[]
            df = pd.DataFrame(columns=['Brand', 'Model',"Price(LKR)","Price Difference"])
            for phone in mobile_phones:
                if phone['os'] == preferences['os']:
                    alternative_phones.append(phone)
            for phone in alternative_phones:
                price_lkr = phone['price']*conversion_rate
                price_diff = abs(price_lkr - preferences['budget'])
                diff_list.append(price_diff)
                df = df.append({'Brand': phone['brand'],'Model':phone['model'], "Price(LKR)":price_lkr,"Price Difference":price_diff}, ignore_index=True)
                #st.write(f"Brand: {phone['brand']}, Model: {phone['model']}, Price: LKR {price_lkr}, Price Difference: LKR {price_diff}")
            column1_sum = df['Price Difference'].sum()
            df['Price Difference2'] = (1-df['Price Difference'] / column1_sum) * 100
            df['Price Difference2'] = df['Price Difference2'].replace(0, 100)
            column2_sum = df['Price Difference2'].sum()
            df['Recommendation Probability'] = (df['Price Difference2'] / column2_sum)
            sorted_df = df.sort_values(by='Recommendation Probability',ascending=False)
            sorted_df = sorted_df.drop(['Price Difference2',"Price Difference"], axis=1)
            st.write(sorted_df.head(4))

if __name__ == '__main__':
    main()

