FROM python:3.10
# Or any preferred Python version.
COPY . .
# ADD main.py .
RUN pip install -r requirements.txt
CMD python main.py
# Or enter the name of your unique directory and parameter set.
