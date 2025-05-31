# PDFTextInspector

**PDFTextInspector** �́APDF�t�@�C������e�L�X�g�𒊏o���A�t�H���g�T�C�Y����W�����ƂɁu���o���v�u���X�g�v�Ȃǂ��������ʂ��A�\�������ꂽ�e�L�X�g�iMarkdown���j���o�͂���GUI�A�v���P�[�V�����ł��B

## ����

- �t�H���g�T�C�Y�ȂǂɊ�Â����o�����x������������
- ���X�g�`���i�ӏ������E�ԍ��t���j�����o�i���K�\���j
- INI�t�@�C���Ō��o���[����������x�J�X�^�}�C�Y�\
- GUI�ŊȒP����
- �\�������ꂽ�e�L�X�g�� `.txt` �t�@�C���Ƃ��ĕۑ�

## GUI�X�N���[���V���b�g

![GUI](https://raw.githubusercontent.com/WAKU-TAKE-A/PDFTextInspector/refs/heads/main/screeshot01.jpg)

## �g�p���@

1. ���̃��|�W�g�����N���[���܂��̓_�E�����[�h
2. �K�v�ȃ��C�u�������C���X�g�[��:
    ```bash
    pip install pymupdf ttkbootstrap
    ```
3. �A�v�����N��:
    ```bash
    python PDFTextInspector.py
    ```
4. GUI����PDF�t�@�C����I��
5. �C�ӂ̃y�[�W�ԍ�����͂���[���]�Ńt�H���g�T�C�Y��ʒu�𒲂ׂ܂��B
6. ini�t�@�C����ҏW���܂��B
7. [�S�e�L�X�g�o��]�ō\�����e�L�X�g��ۑ�

## �o�̓t�@�C��

- ���͂���PDF�Ɠ����t�H���_�ɁA�\�������ꂽ�e�L�X�g�t�@�C���i��: `document.txt`�j���ۑ�����܂��B

## ���[���̃J�X�^�}�C�Y

`PDFTextInspector.ini` �Ƃ���INI�t�@�C���ɂāA�ȉ��̂悤�Ȓ��o���[����ύX�ł��܂�

```ini
[Rules]

; ���p���錩�o���̐ݒ�
enabled_heading_levels = 1,2,3,4,5

; �w�肵���y�[�W�̎w��͈͂̕�������^�C�g�� (#) 
big_heading_page = 1
big_heading_x_min = 20.0
big_heading_x_max = 100.0
big_heading_y_min = 300.0
big_heading_y_max = 500.0

; �匩�o�� (##) �̃t�H���g�T�C�Y�͈�
chapter_min_size = 100.0
chapter_max_size = 200.0

; �����o�� (###) �̃t�H���g�T�C�Y�͈�
small_heading_min_size = 17.8
small_heading_max_size = 18.2

; �����o�� (####) �̃t�H���g�T�C�Y�͈�
lower_heading_min_size = 14.8
lower_heading_max_size = 15.2

; �������o�� (#####) �̃t�H���g�T�C�Y�͈�
lower2_heading_min_size = 13.8
lower2_heading_max_size = 14.2

; �������X�g�̓������}�b�`�p���K�\���p�^�[��
unordered_list_pattern = ^�E

; �L�����X�g�̓������}�b�`�p���K�\���p�^�[��
ordered_list_pattern = ^\d

; �y�[�W���ŏ��O����̈�i�e�L�X�g�̃u���b�N�̍�����W���A���̐ݒ��莆�ʂ̊O���ɂ���ꍇ�͏��O�j
ignore_left_pt = 0
ignore_right_pt = 20
ignore_top_pt = 20
ignore_bottom_pt = 50

; �e�L�X�g�̃u���b�N�̏㉺�֌W�������ƍl����͈�
line_group_threshold = 5.0
```

## �ˑ����C�u����

- PyMuPDF (fitz)
- ttkbootstrap

## ���C�Z���X

MIT License

## �⑫

* �{�c�[���͕��͒��S��PDF��ΏۂƂ��Ă��܂��B�摜���S��PDF��X�L����PDF�ɂ͑Ή����Ă��܂���B
* �e�L�X�g�\���̒��o���[���͕����̃t�H�[�}�b�g�ɂ�蒲�����K�v�ȏꍇ������܂��B