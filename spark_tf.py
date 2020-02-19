def main():
    

if __name__ == '__main__':
    try:
        this = create_session()
        df = this.read.format("mongo").load()
        print(df.show(n=50))
    except protocol.Py4JJavaError:
        print("Error.")
    