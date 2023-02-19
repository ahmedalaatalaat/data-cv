from django.http import HttpResponse
from django.shortcuts import render
from plotly.offline import plot
import plotly.express as px
from .models import Genre
import pandas as pd
import numpy as np


def books_perspective(request):
    df = pd.read_csv('books_project/data/cleaned_goodreads_data.csv')
    genres = Genre.objects.all()
    
    # preprocessing
    df['publication_info'] = pd.to_datetime(df['publication_info'])
    
    if request.GET.get('genre'):
        df = df[df['main_genre'] == request.GET.get('genre')]
    
    # top 15 books
    new_df = df.sort_values('number_of_5_stars_rating', ascending=False)
    new_df.drop_duplicates(subset='title', inplace=True)
    top_15_loved_books = px.bar(new_df.head(15), y='title', x='number_of_5_stars_rating', title="Top 15 Loved Books", text_auto=True, orientation='h')
    top_15_loved_books.update_layout(yaxis={'categoryorder':'total ascending'})
    top_15_loved_books = plot(top_15_loved_books, output_type="div")
    
    # top 10 currently reading books
    new_df = df.sort_values('currently_reading', ascending=False)
    new_df.drop_duplicates(subset='title', inplace=True)
    top_10_currently_reading_books = px.bar(new_df.head(10), x='title', y='currently_reading', color='publisher', text_auto=True, title="Top 10 Books Currently Reading", color_discrete_sequence=px.colors.qualitative.Antique)
    top_10_currently_reading_books.update_layout(xaxis={'categoryorder':'total descending'})
    top_10_currently_reading_books.update(layout_showlegend=False)
    top_10_currently_reading_books = plot(top_10_currently_reading_books, output_type="div")
    
    # top 10 to read
    new_df = df.sort_values('to_read', ascending=False)
    new_df.drop_duplicates(subset='title', inplace=True)
    top_10_to_read_books = px.bar(new_df.head(10), x='title', y='to_read', color='publisher', text_auto=True, title="Top 10 Books To Read", color_discrete_sequence=px.colors.qualitative.Prism)
    top_10_to_read_books.update_layout(xaxis={'categoryorder':'total descending'})
    top_10_to_read_books.update(layout_showlegend=False)
    top_10_to_read_books = plot(top_10_to_read_books, output_type="div")
    
    # book publication over years
    new_df = df.copy(deep=True)
    new_df['published_year'] = new_df['publication_info'].apply(lambda date: date.year)
    new_df_books = new_df.groupby(['published_year'])['goodreads_id'].count().reset_index().sort_values('published_year')
    book_publication_over_years = px.line(new_df_books, x='published_year',y='goodreads_id', range_x=[1950,2023], title='Books Publication over years')
    book_publication_over_years.update_xaxes(
        ticktext=[i for i in range(1950, 2024, 2)],
        tickvals=[i for i in range(1950, 2024, 2)],
    )
    book_publication_over_years = plot(book_publication_over_years, output_type="div")

    # rating distribution
    new_df = df.copy(deep=True)
    new_df.drop_duplicates(subset='title', inplace=True)
    number_of_5_stars_rating = 0
    number_of_4_stars_rating = 0
    number_of_3_stars_rating = 0
    number_of_2_stars_rating = 0
    number_of_1_stars_rating = 0
    for index, row in new_df.iterrows():
        number_of_5_stars_rating += row['number_of_5_stars_rating']
        number_of_4_stars_rating += row['number_of_4_stars_rating']
        number_of_3_stars_rating += row['number_of_3_stars_rating']
        number_of_2_stars_rating += row['number_of_2_stars_rating']
        number_of_1_stars_rating += row['number_of_1_stars_rating']
    rating_data = {
        'number_of_5_stars_rating':number_of_5_stars_rating,
        'number_of_4_stars_rating':number_of_4_stars_rating,
        'number_of_3_stars_rating':number_of_3_stars_rating,
        'number_of_2_stars_rating':number_of_2_stars_rating,
        'number_of_1_stars_rating':number_of_1_stars_rating,
    }
    rating_data_series = pd.Series(rating_data)
    rating_distribution = px.pie(rating_data_series, rating_data_series.index, rating_data_series.values, title="Rating Distribution")
    rating_distribution = plot(rating_distribution, output_type="div")
    
    # wort 10 books
    new_df = df.copy(deep=True)
    new_df.drop_duplicates(subset='title', inplace=True)
    genre_df = new_df.sort_values('number_of_1_stars_rating', ascending=False).head(10)
    worst_15_books = px.bar(genre_df.head(15), y='title', x='number_of_1_stars_rating', text_auto=True, title="Top 15 Books with Negative Reviews", color_discrete_sequence=px.colors.qualitative.Dark24, orientation='h')
    worst_15_books.update_layout(yaxis={'categoryorder':'total descending'})
    worst_15_books = plot(worst_15_books, output_type="div")
    
    context = {
        'genres': genres,
        'top_15_loved_books':top_15_loved_books,
        'top_10_currently_reading_books':top_10_currently_reading_books,
        'top_10_to_read_books':top_10_to_read_books,
        'book_publication_over_years':book_publication_over_years,
        'rating_distribution':rating_distribution,
        'worst_15_books':worst_15_books,
    }
    return render(request, 'books_project/books_perspective.html', context)


def authors_perspective(request):
    df = pd.read_csv('books_project/data/cleaned_goodreads_data.csv')
    genres = Genre.objects.all()
    
    # preprocessing
    df['publication_info'] = pd.to_datetime(df['publication_info'])
    
    if request.GET.get('genre'):
        df = df[df['main_genre'] == request.GET.get('genre')]
    
    # Top 15 Authors
    new_df = df.copy(deep=True)
    new_df.drop_duplicates(subset='title', inplace=True)
    new_df = new_df.groupby('author_name')['number_of_5_stars_rating'].sum().reset_index().sort_values('number_of_5_stars_rating', ascending=False)
    top_15_authors = px.bar(new_df.head(15), y='author_name', x='number_of_5_stars_rating', orientation='h', text_auto=True,color_discrete_sequence=px.colors.qualitative.Antique, title="Top 15 Loved authors")
    top_15_authors.update_layout(yaxis={'categoryorder':'total ascending'})
    top_15_authors = plot(top_15_authors, output_type="div")
    
    # Authors with the most to read
    new_df = df.copy(deep=True)
    new_df.drop_duplicates(subset='title', inplace=True)
    new_df = new_df.groupby('author_name')['to_read'].sum().reset_index().sort_values('to_read', ascending=False)
    authors_with_most_to_read_books = px.bar(new_df.head(10), x='author_name', y='to_read', text_auto=True, title="Authors with the most to read books")
    authors_with_most_to_read_books.update_layout(xaxis={'categoryorder':'total descending'})
    authors_with_most_to_read_books = plot(authors_with_most_to_read_books, output_type="div")
    
    # Authors with the currently reading
    new_df = df.copy(deep=True)
    new_df.drop_duplicates(subset='title', inplace=True)
    new_df = new_df.groupby('author_name')['currently_reading'].sum().reset_index().sort_values('currently_reading', ascending=False)
    authors_with_most_currently_reading_books = px.histogram(new_df.head(10), x='author_name', y='currently_reading', text_auto=True, title="Authors with the most currently reading books")
    authors_with_most_currently_reading_books.update_layout(xaxis={'categoryorder':'total descending'})
    authors_with_most_currently_reading_books = plot(authors_with_most_currently_reading_books, output_type="div")
    
    # Authors with most books published
    new_df = df.sort_values('author_no_of_books', ascending=False)
    new_df.drop_duplicates(subset='author_name', keep='first', inplace=True)
    new_df[['author_name', 'author_no_of_books']].head(10)
    authors_with_most_books = px.scatter(new_df.head(10), 'author_name', 'author_no_of_books', size="author_followers", color='author_followers', size_max=65, title="Authors with the most published books")
    authors_with_most_books = plot(authors_with_most_books, output_type="div")
    
    # Authors with most followers
    new_df = df.sort_values('author_followers', ascending=False)
    new_df.drop_duplicates(subset='author_name', keep='first', inplace=True)
    authors_with_most_followers = px.scatter(new_df.head(10), x='author_name', y='author_followers', title="Authors with the most followers")
    authors_with_most_followers = plot(authors_with_most_followers, output_type="div")
    
    # Top 10 loved translators
    new_df = df[df['is_translated'] == True].copy(deep=True)
    new_df = new_df.groupby('translator')['number_of_5_stars_rating'].sum().reset_index().sort_values('number_of_5_stars_rating', ascending=False)
    top_10_translators = px.bar(new_df.head(10), y='translator', x='number_of_5_stars_rating', orientation='h', text_auto=True,color_discrete_sequence=px.colors.qualitative.T10, title="Top 10 Loved Translators")
    top_10_translators.update_layout(yaxis={'categoryorder':'total ascending'})
    top_10_translators = plot(top_10_translators, output_type="div")
    
    
    context = {
        'genres': genres,
        'top_15_authors':top_15_authors,
        'authors_with_most_to_read_books':authors_with_most_to_read_books,
        'authors_with_most_currently_reading_books':authors_with_most_currently_reading_books,
        'authors_with_most_books':authors_with_most_books,
        'authors_with_most_followers':authors_with_most_followers,
        'top_10_translators':top_10_translators,
    }
    return render(request, 'books_project/authors_perspective.html', context)


def load_data_to_database(request):
    data = pd.read_csv('books_project/data/cleaned_goodreads_data.csv')

    my_genres = data.groupby('main_genre')['goodreads_id'].count().reset_index()
    genres = []
    for index, genre in my_genres['main_genre'].items():
        my_genre = Genre(
            name=str(genre)
        )
        genres.append(my_genre)
    
    Genre.objects.bulk_create(genres)
    return HttpResponse('Done')

