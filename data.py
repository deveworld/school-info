class Types:
    S_INFO  = "SPECIAL_INFO"
    S_NODP  = "SPECIAL_NODISPLAY"
    LESSON  = "LESSON"
    RECESS  = "RECESS"

class Screens:
    REMAIN  = 0
    LESSON  = 1
    NOTICE  = 2
    TTABLE  = 3
    INFO    = 4

Notice = "현재 공지가 없습니다."

Lessons = {
    "Mon": {
        "1교시":  {"subject": "과학", "teacher": "이장희"}, # 1교시
        "2교시":  {"subject": "일본어", "teacher": "쿠라타 케이시"}, # 2교시
        "3교시":  {"subject": "과학", "teacher": "이정호"}, # 3교시
        "4교시":  {"subject": "일본어", "teacher": "김규만"}, # 4교시
        "5교시": {"subject": "한국사", "teacher": "이용제"}, # 5교시
        "6교시": {"subject": "심화회화", "teacher": "Thomas Hackney"}, # 6교시
        "7교시": {"subject": "수학", "teacher": "이휘재"}, # 7교시
        "야자1": {"subject": "야자1", "teacher": "-"},
        "야자2": {"subject": "야자2", "teacher": "-"},
    },
    "Tue": {
        "1교시":  {"subject": "영어", "teacher": "표유미"}, # 1교시
        "2교시":  {"subject": "국어", "teacher": "정채현"}, # 2교시
        "3교시":  {"subject": "과학", "teacher": "이상국"}, # 3교시
        "4교시":  {"subject": "사회", "teacher": "전정재"}, # 4교시
        "5교시": {"subject": "진로", "teacher": "황효순"}, # 5교시
        "6교시": {"subject": "수학", "teacher": "이휘재"}, # 6교시
        "7교시": {"subject": "일본어", "teacher": "김규만"}, # 7교시
        "야자1": {"subject": "야자1", "teacher": "-"},
        "야자2": {"subject": "야자2", "teacher": "-"},
    },
    "Wed": {
        "1교시":  {"subject": "체육", "teacher": "박수경"}, # 1교시
        "2교시":  {"subject": "수학", "teacher": "이휘재"}, # 2교시
        "3교시":  {"subject": "심화회화", "teacher": "Thomas Hackney"}, # 3교시
        "4교시":  {"subject": "한국사", "teacher": "이용제"}, # 4교시
        "5교시": {"subject": "HR", "teacher": "-"}, # 5교시
        "6교시": {"subject": "창체", "teacher": "-"}, # 6교시
        "7교시": {"subject": "창체", "teacher": "-"}, # 7교시
        "야자1": {"subject": "야자1", "teacher": "-"},
        "야자2": {"subject": "야자2", "teacher": "-"},
    },
    "Thu": {
        "1교시":  {"subject": "국어", "teacher": "정채현"}, # 1교시
        "2교시":  {"subject": "일본어", "teacher": "김규만"}, # 2교시
        "3교시":  {"subject": "사회", "teacher": "이건상"}, # 3교시
        "4교시":  {"subject": "영어", "teacher": "정유선"}, # 4교시
        "5교시": {"subject": "일본어", "teacher": "쿠라타 케이시"}, # 5교시
        "6교시": {"subject": "체육", "teacher": "박수경"}, # 6교시
        "7교시": {"subject": "과학탐구", "teacher": "이정호"}, # 7교시
        "야자1": {"subject": "야자1", "teacher": "-"},
        "야자2": {"subject": "야자2", "teacher": "-"},
    },
    "Fri": {
        "1교시":  {"subject": "일본어", "teacher": "김규만"}, # 1교시
        "2교시":  {"subject": "영어", "teacher": "정유선"}, # 2교시
        "3교시":  {"subject": "심화회화", "teacher": "김창현"}, # 3교시
        "4교시":  {"subject": "사회", "teacher": "이건상"}, # 4교시
        "5교시": {"subject": "국어", "teacher": "정채현"}, # 5교시
        "6교시": {"subject": "음악", "teacher": "문영모"}, # 6교시
        "7교시": {"subject": "한국사", "teacher": "이용제"}, # 7교시
        "야자1": {"subject": "야자1", "teacher": "-"},
        "야자2": {"subject": "야자2", "teacher": "-"},
    }
}

Times = [
    {"name": "등교이전",    "time": "00/00", "type": Types.S_NODP},
    {"name": "등교중",      "time": "07/30", "type": Types.S_INFO, "display": "어서오세요.\n오늘은 {}년 {}월 {}일 ({}) 입니다."},
    {"name": "등교",        "time": "08/00", "type": Types.S_INFO, "display": "어서오세요.\n오늘은 {}년 {}월 {}일 ({}) 입니다.\n등교 시간은 {}까지 입니다."},
    {"name": "종례",        "time": "08/10", "type": Types.RECESS},
    {"name": "1교시",       "time": "09/00", "type": Types.LESSON},
    {"name": "1휴식",       "time": "09/10", "type": Types.RECESS},
    {"name": "2교시",       "time": "10/00", "type": Types.LESSON},
    {"name": "2휴식",       "time": "10/10", "type": Types.RECESS},
    {"name": "3교시",       "time": "11/00", "type": Types.LESSON},
    {"name": "점심",        "time": "12/00", "type": Types.RECESS},
    {"name": "4교시",       "time": "12/50", "type": Types.LESSON},
    {"name": "4휴식",       "time": "13/00", "type": Types.RECESS},
    {"name": "5교시",       "time": "13/50", "type": Types.LESSON},
    {"name": "5휴식",       "time": "14/00", "type": Types.RECESS},
    {"name": "6교시",       "time": "14/50", "type": Types.LESSON},
    {"name": "6휴식",       "time": "15/00", "type": Types.RECESS},
    {"name": "7교시",       "time": "15/50", "type": Types.LESSON},
    {"name": "종례",        "time": "16/10", "type": Types.RECESS},
    {"name": "1야자",       "time": "17/00", "type": Types.LESSON},
    {"name": "저녁",        "time": "18/00", "type": Types.RECESS},
    {"name": "2야자",       "time": "20/55", "type": Types.LESSON},
    {"name": "하교",        "time": "21/00", "type": Types.S_INFO, "display": "안녕히 가십시오.\n내일은 {}년 {}월 {}일 ({}) 입니다."},
    {"name": "하교이후",    "time": "23/59", "type": Types.S_NODP}
]
