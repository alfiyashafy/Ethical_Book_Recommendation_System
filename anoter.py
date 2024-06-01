import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Streamlit page configuration
st.set_page_config(layout='wide', page_title='Book Recommendation System')

# Load datasets with appropriate data types to avoid warnings
books = pd.read_csv('Books.csv', dtype={'Year-Of-Publication': str, 'Book-Author': str})
users = pd.read_csv('Users.csv')
ratings = pd.read_csv('Ratings.csv')

# Merging data
ratings_with_name = ratings.merge(books, on='ISBN')

num_rating_df = ratings_with_name.groupby('Book-Title').count()['Book-Rating'].reset_index()
num_rating_df.rename(columns={'Book-Rating': 'num_ratings'}, inplace=True)

avg_rating_df = ratings_with_name.groupby('Book-Title')['Book-Rating'].mean().reset_index()
avg_rating_df.rename(columns={'Book-Rating': 'avg_rating'}, inplace=True)

popularity_df = num_rating_df.merge(avg_rating_df, on='Book-Title')

popular_df = popularity_df[popularity_df['num_ratings'] > 250].sort_values('avg_rating', ascending=False).head(50)
popular_df = popular_df.merge(books, on='Book-Title').drop_duplicates('Book-Title')[
    ['Book-Title', 'Book-Author', 'Year-Of-Publication', 'num_ratings', 'avg_rating']]


def load_overall_analysis():
    st.title('Top 50 Books')
    st.dataframe(popular_df)


# Collaborative Filtering Based Recommender System
x = ratings_with_name.groupby('User-ID').count()['Book-Rating'] > 200
exp_users = x[x].index
filtered_rating = ratings_with_name[ratings_with_name['User-ID'].isin(exp_users)]
y = filtered_rating.groupby('Book-Title').count()['Book-Rating'] >= 50
famous_books = y[y].index
final_ratings = filtered_rating[filtered_rating['Book-Title'].isin(famous_books)]
pt = final_ratings.pivot_table(index='Book-Title', columns='User-ID', values='Book-Rating')
pt.fillna(0, inplace=True)
similarity_score = cosine_similarity(pt)


# Another Recommendation Algorithm
# using a popularity-based recommender
def popularity_recommendation(num_recommendations=5):
    popular_books = popularity_df.sort_values('num_ratings', ascending=False).head(num_recommendations)
    return popular_books['Book-Title'].tolist()


def recommend(book_name, user_id, num_recommendations=5):
    if book_name in pt.index:
        index = np.where(pt.index == book_name)[0][0]
        similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)

        # Get the list of books the user has already read
        user_read_books = ratings[ratings['User-ID'] == user_id]['Book-Title'].unique()

        # Filter out the already read books from the recommendations
        recommended_books = []
        for item in similar_items:
            if pt.index[item[0]] not in user_read_books and pt.index[item[0]] != book_name:
                recommended_books.append(pt.index[item[0]])
            if len(recommended_books) == num_recommendations:
                break

        return recommended_books
    else:
        return popularity_recommendation(num_recommendations)  # Fallback to popularity-based recommendations


def get_author_recommendations(user_id, author_name, num_recommendations=3):
    author_books = books[books['Book-Author'] == author_name]['ISBN'].unique()
    author_ratings = ratings[ratings['ISBN'].isin(author_books)]
    user_ratings = author_ratings[author_ratings['User-ID'] == user_id]
    unrated_books = pd.Series(author_books)[~pd.Series(author_books).isin(user_ratings['ISBN'])]
    avg_ratings = author_ratings.groupby('ISBN')['Book-Rating'].mean().reset_index()
    top_books = avg_ratings.sort_values(by='Book-Rating', ascending=False)
    top_books = top_books[top_books['ISBN'].isin(unrated_books)]
    top_recommendations = top_books.head(num_recommendations)
    return top_recommendations


# Streamlit UI
st.sidebar.title('Book Recommendation System')

# User ID input
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None

if st.session_state['user_id'] is None:
    user_id = st.sidebar.text_input('Enter User ID')
    if user_id:
        st.session_state['user_id'] = user_id
else:
    user_id = st.session_state['user_id']
    st.sidebar.write(f'User ID: {user_id}')

    # Recommendation options using radio buttons
    option = st.sidebar.radio('Select One', ['Top 50 Books', 'Recommendation Based'])

    if option == 'Top 50 Books':
        load_overall_analysis()
    else:
        user_books = ratings[ratings['User-ID'] == int(user_id)]['ISBN'].unique()
        selected_author = st.sidebar.selectbox('Select Author', sorted(set(books['Book-Author'].dropna())))

        if selected_author:
            author_recommendations = get_author_recommendations(int(user_id), selected_author)
            st.title(f'Top {len(author_recommendations)} recommendations for {selected_author}')

            if not author_recommendations.empty:
                selected_books = st.radio(
                    'Select a book',
                    options=author_recommendations['ISBN'].tolist(),
                    format_func=lambda
                        x: f"ISBN: {x}, Average Rating: {author_recommendations[author_recommendations['ISBN'] == x]['Book-Rating'].values[0]}"
                )

                book_details = books[books['ISBN'] == selected_books]

                st.write('### Book Details:')
                st.write(f"**Title:** {book_details['Book-Title'].values[0]}")
                st.write(f"**Author:** {book_details['Book-Author'].values[0]}")
                st.write(f"**Year:** {book_details['Year-Of-Publication'].values[0]}")
                st.write(f"**Publisher:** {book_details['Publisher'].values[0]}")
                st.image(book_details['Image-URL-L'].values[0], width=150)

                # Read Again and Recommend New options
                action = st.radio('Action', ['Read Again', 'Recommend New'])

                if action == 'Read Again':
                    st.write('### Book Details:')
                    st.write(f"**Title:** {book_details['Book-Title'].values[0]}")
                    st.write(f"**Author:** {book_details['Book-Author'].values[0]}")
                    st.write(f"**Year:** {book_details['Year-Of-Publication'].values[0]}")
                    st.write(f"**Publisher:** {book_details['Publisher'].values[0]}")
                    st.image(book_details['Image-URL-L'].values[0], width=150)

                elif action == 'Recommend New':

                    new_recommendations = recommend(book_details['Book-Title'].values[0], int(user_id),
                                                    num_recommendations=5)
                    if new_recommendations:
                        st.write('### New Recommendations:')
                        for book_title in new_recommendations:
                            new_book_details = books[books['Book-Title'] == book_title]
                            st.write(f"**Title:** {new_book_details['Book-Title'].values[0]}")
                            st.write(f"**Author:** {new_book_details['Book-Author'].values[0]}")
                            st.write(f"**Year:** {new_book_details['Year-Of-Publication'].values[0]}")
                            st.write(f"**Publisher:** {new_book_details['Publisher'].values[0]}")
                            st.image(new_book_details['Image-URL-L'].values[0], width=150)
                            st.write('---')
                    else:
                        st.write('### No similar books found for further recommendation.')
                        st.write('### However, here are some alternative ways to discover new books:')
                        st.write('- Explore different genres or authors.')
                        st.write('- Refine search criteria and specify preferences.')
                        st.write('- Check out top charts or curated lists.')
                        st.write('- Seek recommendations from peers or experts.')
                        st.write('- Try different recommendation algorithms.')
                        st.write('- Join online communities dedicated to literature.')
