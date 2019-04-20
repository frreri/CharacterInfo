from webengine import create_app
#from flask import Flask, render_template, request, redirect, Response, jsonify, abort, flash, url_for
#import random, json

app = create_app()

if __name__ == "__main__":
    app.run("127.0.0.1")
