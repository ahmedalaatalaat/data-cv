from django.http import HttpResponse
from django.shortcuts import render
from plotly.offline import plot
import plotly.express as px
import pandas as pd
import numpy as np


def netflix_titles(request):
    df = pd.read_csv('netflix_project/data/netflix_titles.csv')
    
    # data preprocessing
    country_names = df['country'].astype(str)
    df['main_country'] = [i.split(",")[0].strip() for i in country_names]
    df['date_added'] = pd.to_datetime(df['date_added'])
    df['year_added'] = df['date_added'].apply(lambda date: date.year)
    
    # Total movies & TV shows by country
    new_df = df.groupby('main_country')['show_id'].count().reset_index().sort_values('show_id', ascending=False)
    new_df.rename(columns={'show_id': 'number_of_shows'}, inplace=True)
    
    total_titles_by_country = px.choropleth(new_df, locations="main_country", color="number_of_shows",  locationmode='country names', title = 'Total movies & TV shows by country', color_continuous_scale=['#ffa98e','#de1500'])
    total_titles_by_country.update_layout(
        title="<b>Total movies & TV shows by country</b>",
        template='seaborn',
        paper_bgcolor="#000000",
        font_color="#FFFFFF",
        title_font_color="#de1500",
        title_font=dict(
            size=22,
        ),
        legend=dict(
            orientation="v",
            yanchor="auto",
            y=1.02,
            xanchor="right",
            x=1),
        geo=dict(
            bgcolor= '#2b2b2b', 
            landcolor='#000000', 
            showlakes=False))
    total_titles_by_country = plot(total_titles_by_country, output_type="div")
    
    
    # Rating distribution
    rating_distribution = px.histogram(df, 'rating', text_auto=True, color_discrete_sequence=['#de1500'], title="Ratings")
    rating_distribution.update_layout(
        title='<b>Ratings</b>',
        xaxis_title="",
        yaxis_title="",
        template='seaborn',
        paper_bgcolor="#000000",
        font_color="#FFFFFF",
        xaxis={'categoryorder':'total descending', 'showgrid': False},
        yaxis={'showgrid': False},
        plot_bgcolor='#000000',
        title_font_color="#de1500",
        title_font=dict(
            size=22,
        ))
    rating_distribution = plot(rating_distribution, output_type="div")
    
    
    # Movies & TV show distribution
    new_df = df.groupby('type')['show_id'].count().reset_index().sort_values('show_id', ascending=False)
    new_df.rename(columns={'show_id': 'number_of_shows'}, inplace=True)
    
    movies_tv_distribution = px.scatter(new_df, 'type', 'type', size='number_of_shows', size_max=100, color="number_of_shows", text='number_of_shows', color_continuous_scale = ['#ffa98e','#de1500'])
    movies_tv_distribution.update_layout(
        title='<b>Movies & TV show distribution</b>',
        xaxis_title="",
        template='seaborn',
        paper_bgcolor="#000000",
        font_color="#FFFFFF",
        xaxis={'categoryorder':'total ascending', 'showgrid': False, 'visible': True},
        yaxis={'showgrid': False, 'visible': False,},
        coloraxis_showscale=False,
        plot_bgcolor='#000000',
        title_font_color="#de1500",
        title_font=dict(
            size=22,
        ))
    movies_tv_distribution = plot(movies_tv_distribution, output_type="div")
    
    
    # Top 10 genres
    new_df = df.groupby('listed_in')['show_id'].count().reset_index().sort_values('show_id', ascending=False)
    new_df.rename(columns={'show_id': 'number_of_shows'}, inplace=True)
    
    top_10_genres = px.histogram(new_df.head(10), x='number_of_shows', y='listed_in', title='Top 10 genres', color_discrete_sequence=['#de1500'],text_auto=True)
    top_10_genres.update_layout(
        title='<b>Top 10 genres</b>',
        xaxis_title="",
        yaxis_title="",
        template='seaborn',
        paper_bgcolor="#000000",
        font_color="#FFFFFF",
        xaxis={'showgrid': False,},
        yaxis={'categoryorder':'total ascending', 'showgrid': False},
        plot_bgcolor='#000000',
        title_font_color="#de1500",
        title_font=dict(
            size=22,
        ))
    top_10_genres = plot(top_10_genres, output_type="div")
    
    
    # Total movies & Tv shows by years
    new_df = df.groupby(['year_added', 'type'])['show_id'].count().reset_index().sort_values('year_added', ascending=False)
    new_df.rename(columns={'show_id': 'number_of_shows'}, inplace=True)
    
    total_titles_by_years = px.area(new_df, 'year_added', 'number_of_shows', color='type', color_discrete_sequence=['#ffa98e','#de1500'], title='Total movies & Tv shows by years', text='number_of_shows')
    total_titles_by_years.update_layout(
        title='<b>Total movies & Tv shows by years</b>',
        xaxis_title="",
        yaxis_title="",
        template='seaborn',
        paper_bgcolor="#000000",
        font_color="#FFFFFF",
        xaxis={'showgrid': False,},
        yaxis={'categoryorder':'total ascending', 'showgrid': False},
        plot_bgcolor='#000000',
        title_font_color="#de1500",
        title_font=dict(
            size=22,
        ))
    total_titles_by_years.update_xaxes(
        ticktext=[i for i in range(2008, 2022)],
        tickvals=[i for i in range(2008, 2022)],
    )
    total_titles_by_years = plot(total_titles_by_years, output_type="div")
    
    
    
    context = {
        'total_titles_by_country':total_titles_by_country,
        'rating_distribution':rating_distribution,
        'movies_tv_distribution':movies_tv_distribution,
        'top_10_genres':top_10_genres,
        'total_titles_by_years':total_titles_by_years,
    }
    
    return render(request, 'netflix_project/netflix_titles.html', context)