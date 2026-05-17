from enum import Enum
from htmlnode import ParentNode, LeafNode
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    # Split the document by double newlines
    raw_blocks = markdown.split("\n\n")
    filtered_blocks = []
    
    for block in raw_blocks:
        # Strip leading and trailing whitespace from the block
        stripped_block = block.strip()
        # Only keep the block if it isn't completely empty
        if stripped_block != "":
            filtered_blocks.append(stripped_block)
            
    return filtered_blocks

def block_to_block_type(block):
    # Headings check (1 to 6 '#' followed by a space)
    if (
        block.startswith("# ")
        or block.startswith("## ")
        or block.startswith("### ")
        or block.startswith("#### ")
        or block.startswith("##### ")
        or block.startswith("###### ")
    ):
        return BlockType.HEADING

    # Code blocks check (starts and ends with 3 backticks)
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # Multi-line blocks require line-by-line inspection
    lines = block.split("\n")

    # Quote block check (every line must start with '>')
    if block.startswith(">"):
        if all(line.startswith(">") for line in lines):
            return BlockType.QUOTE

    # Unordered list check (every line must start with '- ')
    if block.startswith("- "):
        if all(line.startswith("- ") for line in lines):
            return BlockType.UNORDERED_LIST

    # Ordered list check (every line must start with incrementing numbers '1. ', '2. ', etc.)
    if block.startswith("1. "):
        is_ordered_list = True
        for i, line in enumerate(lines):
            expected_prefix = f"{i + 1}. "
            if not line.startswith(expected_prefix):
                is_ordered_list = False
                break
        if is_ordered_list:
            return BlockType.ORDERED_LIST

    # If it matches no special rules, it's a default paragraph
    return BlockType.PARAGRAPH

def text_to_children(text):
    """
    Helper function to convert a raw string containing inline markdown
    into a list of HTMLNode child objects.
    """
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    
    for block in blocks:
        b_type = block_to_block_type(block)
        
        if b_type == BlockType.PARAGRAPH:
            # Soft wraps (newlines within a paragraph) become spaces in HTML
            text = block.replace("\n", " ")
            children = text_to_children(text)
            block_nodes.append(ParentNode("p", children))
            
        elif b_type == BlockType.HEADING:
            # Calculate heading level by counting leading '#'
            level = 0
            for char in block:
                if char == '#':
                    level += 1
                else:
                    break
            # Extract content text after the hashes and the space
            text = block[level + 1:]
            children = text_to_children(text)
            block_nodes.append(ParentNode(f"h{level}", children))
            
        elif b_type == BlockType.CODE:
            # Slices out the opening and closing ```
            text = block[3:-3]
            if text.startswith("\n"):
                text = text[1:]
            # Code blocks bypass inline rules completely per instructions
            code_node = LeafNode("code", text)
            pre_node = ParentNode("pre", [code_node])
            block_nodes.append(pre_node)
            
        elif b_type == BlockType.QUOTE:
            lines = block.split("\n")
            clean_lines = []
            for line in lines:
                if line.startswith("> "):
                    clean_lines.append(line[2:])
                else:
                    clean_lines.append(line[1:])
            text = " ".join(clean_lines)
            children = text_to_children(text)
            block_nodes.append(ParentNode("blockquote", children))
            
        elif b_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            li_nodes = []
            for line in lines:
                text = line[2:] # Strip "- "
                children = text_to_children(text)
                li_nodes.append(ParentNode("li", children))
            block_nodes.append(ParentNode("ul", li_nodes))
            
        elif b_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            li_nodes = []
            for line in lines:
                dot_index = line.find(". ")
                text = line[dot_index + 2:] # Strip "1. ", "2. ", etc.
                children = text_to_children(text)
                li_nodes.append(ParentNode("li", children))
            block_nodes.append(ParentNode("ol", li_nodes))
            
    return ParentNode("div", block_nodes)


