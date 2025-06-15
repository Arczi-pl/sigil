# Sigil (Signature Invisible Layer)

Sigil is a text steganography tool created by Artur Sikorski that allows you to invisibly embed signatures or hidden messages in plain text files and extract them later. The embedding process is done using invisible Unicode characters, making it undetectable to human readers.

## Features

- **Invisible Embedding**: Hide messages within text files without changing their visible appearance
- **Simple CLI Interface**: Easy-to-use command-line interface
- **Unicode-Based**: Uses invisible Unicode characters for steganography
- **Preserves Original Text**: Does not alter the readable content of the document
- **Automatic Length Calculation**: Determines the maximum length of signature that can be embedded

## Installation

### Prerequisites
- Python 3.12 or higher

### From Source
```bash
# Clone the repository
git clone https://github.com/Arczi-pl/sigil.git
cd sigil

# Create a virtual environment and install dependencies
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Embedding a Signature

```bash
./sigil <input_file> "<your_signature>"
```

This will create a new file with the same content but with your signature embedded invisibly. The output file will be named with the suffix `__sigiled` added to the original filename.

Example:
```bash
./sigil examples/lorem_ipsum.txt "created by Artur Sikorski"
```

### Extracting a Signature

```bash
./sigil <sigiled_file>
```

This will extract and display the signature that was embedded in the file.

Example:
```bash
./sigil examples/lorem_ipsum__sigiled.txt
# Output: created by Artur Sikorski
```

## How It Works

Sigil works by:

1. Converting your signature message to a number using UTF-8 encoding
2. Converting that number to a custom base representation (using 3 invisible characters)
3. Using three different invisible Unicode characters (\u200c, \u2062, \u2063) to represent digits in this custom base
4. Inserting these invisible characters between characters of the original text
5. When extracting, the process is reversed to recover the original message

## Examples

The repository includes example files in the `examples/` directory:
- `lorem_ipsum.txt` - A sample text file
- `lorem_ipsum__sigiled.txt` - The same text with an embedded signature
