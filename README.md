# GraphRAG Paper Implementation

## Overview

This repository contains the implementation of the [GraphRAG paper](https://arxiv.org/abs/2404.16130), utilizing the podcast transcript of Dwarkesh Patel as the knowledge source, in following with the [original paper](https://arxiv.org/abs/2404.16130).

To chat and play around with your queries, visit [here](https://graphrag-impl.streamlit.app/).

To visualize the knowledge graph, visit [here](https://israel-adewuyi.github.io/assets/html/network.html).

You could also read my [blog post](https://israel-adewuyi.github.io/blog/2024/replicating-graphrag/) on replicating the [original paper](https://arxiv.org/abs/2404.16130) and the different decisions I made.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Dataset](#dataset)
- [Contributing](#contributing)
- [License](#license)

## Installation

To set up the project locally, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/GraphRAG-Implementation.git
   cd GraphRAG-Implementation
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run**
   ```bash
   streamlit run .\webpages\app.py
   ```

## Dataset

The dataset used in this project is the podcast transcript of Dwarkesh Patel. The transcript is available in the `transcripts` directory. Specifically, I used his [interview with Trenton Bricken and Sholto Douglas](https://www.youtube.com/watch?v=UTuuTTnjxMQ).

## Contributing

Contributions are welcome!

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments

- To the paper authors for their great work!
- To Dwarkesh Patel for making (some) of his podcast transcript available on his website.
