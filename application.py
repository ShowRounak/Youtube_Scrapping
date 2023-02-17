from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import scrapper
import sql
import logging

logging.basicConfig(filename="app.log", level=logging.DEBUG, filemode='w',
                    format="%(asctime)s %(levelname)s %(message)s")

application = Flask(__name__)
app = application


@app.route('/', methods=['GET'])
@cross_origin()
def homepage():
    """Render homepage"""
    return render_template("index.html")


@app.route('/details', methods=['GET', 'POST'])
@cross_origin()
def video_details():
    """This function returns video details and comments"""
    if request.method == 'POST':
        try:
            video_url = request.form['content']
            obj = scrapper.YouTube()
            description = obj.video_description(video_url)
            comments_list = obj.comment_threads(video_url[32:])

            sql_obj = sql.MySQL_operations("localhost", "root", "password", "rikdb")
            sql_obj.create_connection()

            for i in range(len(comments_list)):
                sql_obj.insert_data(
                    "'{title}', '{views}','{likes}','{des}','{author}','{comment}'".format(title=description['TITLE'],
                                                                                           views=description['VIEWS'],
                                                                                           likes=description['LIKES'],
                                                                                           des=description['DESCRIPTION'],
                                                                                           author=comments_list[i][
                                                                                               'Person'],
                                                                                           comment=comments_list[i][
                                                                                               'Comment'].replace("'"," ")))
            logging.info("Successfully scrap video details and comments")
            return render_template('result.html', details=description,reply=comments_list[0:len(comments_list)])
        except Exception as e:
            print("Exception occurred", e)
            logging.error("Exception occurred", e)
    else:
        return render_template("index.html")


@app.route('/uploads', methods=['GET', 'POST'])
@cross_origin()
def total_videos():
    """This function returns the number of total videos uploaded by a specific channel"""
    if request.method == 'POST':
        try:
            channel_url = request.form['content']
            x = scrapper.YouTube()
            no_of_uploads = x.total_videos(channel_url)
            logging.info("Successfully scrap total number of videos")
            return render_template('uploadresult.html', uploads = no_of_uploads)
        except Exception as e:
            print("Exception occurred", e)
            logging.error("Exception occurred", e)
    else:
        return render_template("index.html")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8001, debug=True)
