from distinguish.aip import AipOcr

class apiUtil():

    def handWrittingOCR(path):
        # 定义常量
        APP_ID = '11352343'
        API_KEY = 'Nd5Z1NkGoLDvHwBnD2bFLpCE'
        SECRET_KEY = 'A9FsnnPj1Ys2Gof70SNgYo23hKOIK8Os'

        # 初始化AipFace对象
        aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)

        def get_file_content(path):
            with open(path, 'rb') as fp:
                return fp.read()

        # 定义参数变量
        options = {
            'detect_direction': 'true',
            'language_type': 'CHN_ENG',
        }

        # 调用通用文字识别接口
        result = aipOcr.handwriting(get_file_content(path), options)
        words_result = result['words_result']

        text = ""

        for i in range(len(words_result)):
            text += (words_result[i]['words'] + "\n")

        return text

    def chiOCR(path):
        # 定义常量
        APP_ID = '11352343'
        API_KEY = 'Nd5Z1NkGoLDvHwBnD2bFLpCE'
        SECRET_KEY = 'A9FsnnPj1Ys2Gof70SNgYo23hKOIK8Os'

        # 初始化AipFace对象
        aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)


        def get_file_content(path):
            with open(path, 'rb') as fp:
                return fp.read()


        # 定义参数变量
        options = {
            'detect_direction': 'true',
            'language_type': 'CHN_ENG',
        }

        # 调用通用文字识别接口
        result = aipOcr.basicAccurate(get_file_content(path), options)
        words_result = result['words_result']

        text = ""

        for i in range(len(words_result)):
            text += (words_result[i]['words']+"\n")

        return text
