# Extended JCM (eJCM)
This dataset is an extension of [**JCommonsenseMorality**](https://github.com/Language-Media-Lab/commonsense-moral-ja), a dataset that reflects Japanese commonsense morality.


## Method： Masked Token and Label Enhancement (MTLE)
MTLE is a text extension method and achieves more diverse sentence expansion by replacing important parts of sentences and allowing label changes, leveraging the extensive knowledge of LLMs.
We have extended the existing JCM dataset using MTLE to generate the Extended JCM (eJCM) dataset.

MTLE framework
<p align="center">
  <img src="./figures/mtle.png" alt="MTLE framework" width=512>
</p>


## References
- 竹下昌志, ジェプカ・ラファウ, 荒木健治. JCommonsenseMorality:常識道徳の理解度評価用日本語データセット. 言語処理学会第29回年次大会, pp.357-362, March 2023. [[PDF]](https://www.anlp.jp/proceedings/annual_meeting/2023/pdf_dir/D2-1.pdf)