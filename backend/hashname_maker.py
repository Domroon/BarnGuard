import secrets

    
def main():
    random_name = secrets.token_urlsafe(8)
    print(random_name)

if __name__ == '__main__':
    main()
