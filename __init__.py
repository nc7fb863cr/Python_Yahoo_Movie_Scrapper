import requests,re,os
from bs4 import BeautifulSoup
from flask import Flask,jsonify,request,send_from_directory

from Movielist import get_movie,get_all_movie
