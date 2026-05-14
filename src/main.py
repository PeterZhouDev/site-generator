from textnode import TextNode, TextType

def main():
    # Creating a dummy TextNode instance
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    
    # Printing the object to see the __repr__ output
    print(node)

if __name__ == "__main__":
    main()# hello world
