# dataloader
- conda env create -f environment.yml 로 가상환경 생성 
- conda activate project 로 가상환경 활성화
## dataset download
- pip install kaggle
- kaggle datasets download -d zcyzhchyu/mini-imagenet
- unzip mini-imagenet
- tar -cvf images.tar images
## 필수 주의 사항
- dataloader_ 파일들의 main 문에서 root 주소 바꾸기
- python main.py --batch_size "32" (default batch_size 2) 실행하면 5번 씩 입력한 batch_size에 대해서 default, grid_cutline, binary_cutline, greed_cutline 에 대한 평균 출력
