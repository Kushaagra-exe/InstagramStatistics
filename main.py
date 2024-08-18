import json
import streamlit as st
import pandas as pd
def load_json(file):
    try:
        data = json.load(file)
        return data
    except json.JSONDecodeError:
        st.error("Failed to decode JSON. Please upload a valid JSON file.")
        return None


def extract_values_from_json(followers_json, following_json):
    followers_list = []
    following_list = []

    # followers
    try:
        if isinstance(followers_json, list):
            followers_list = [item['value'] for i in followers_json for item in i.get('string_list_data', [])]
        else:
            st.error("Please Upload the correct followers file")
    except (KeyError, TypeError) as e:
        st.error(f"Error processing followers JSON: {e}")

    #  following
    try:
        if 'relationships_following' in following_json and isinstance(following_json['relationships_following'], list):
            following_list = [item['value'] for entry in following_json['relationships_following'] for item in
                              entry.get('string_list_data', [])]
        else:
            st.error(
                "Please Upload the correct following file")
    except (KeyError, TypeError) as e:
        st.error(f"Error processing following JSON: {e}")

    return followers_list, following_list


def compute_difference(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    return list(set2 - set1)

def add_links(data_list):
    return [{'Username': value, 'Account': f'<a href="https://www.instagram.com/{value}/" target="_blank">Link</a>'} for value in data_list]

def display_with_links(data_list):
    data = add_links(data_list)
    df = pd.DataFrame(data)
    # Convert DataFrame to HTML for rendering
    st.markdown(df.to_html(escape=False), unsafe_allow_html=True)









def main():

    st.title('Instagram Statistics')

    uploaded_file1 = st.file_uploader("Followers JSON file", type="json")
    uploaded_file2 = st.file_uploader("Following JSON file", type="json")
    if uploaded_file1 and uploaded_file2:

            followers_json = load_json(uploaded_file1)
            following_json = load_json(uploaded_file2)

            if followers_json and following_json:
                followers_list, following_list = extract_values_from_json(followers_json, following_json)

                list_to_show = st.radio(
                    "Select the list to display:",
                    ("My Followers", "My Following", "Not Following you back", "You not following back")
                )

                if list_to_show == "My Followers":
                    if followers_list:
                        st.subheader("My Followers")
                        display_with_links(followers_list)
                    else:
                        st.write("No data available for Followers List.")

                elif list_to_show == "My Following":
                    if following_list:
                        st.subheader("My Following")
                        display_with_links(following_list)
                    else:
                        st.write("No data available for Following List.")

                elif list_to_show == "Not Following you back":
                    difference_list = compute_difference(followers_list, following_list)
                    if difference_list:
                        st.subheader("Accounts Not Following you back")
                        display_with_links(difference_list)
                    else:
                        st.write("No data available for Followers List.")

                elif list_to_show == "You not following back":
                    difference_list = compute_difference(following_list, followers_list)
                    if difference_list:
                        st.subheader("Accounts You are not following back")
                        display_with_links(difference_list)

if __name__ == '__main__':
    main()




# followers_list = [item['value'] for i in followers_json for item in i['string_list_data']]
# following_list = [item['value'] for entry in following_json['relationships_following'] for item in entry['string_list_data']]
#
# following_list = set(following_list)
# followers_list = set(followers_list)
#
#
# not_following_back = following_list - followers_list
# print(not_following_back)


