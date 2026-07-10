custom_css = """
<style>
        .stApp {
            background: #ffffff;
            color: #000000;
        }

        div[data-testid="stAppViewContainer"] {
            background: #ffffff;
            color: #000000;
        }

        div[data-testid="stAppViewBlockContainer"] {
            color: #000000;
        }

        section[data-testid="stSidebar"] {
            background: #7a0000;
        }

        section[data-testid="stSidebar"] * {
            color: #ffffff;
        }

        section[data-testid="stSidebar"] .stButton button {
            background: #ffffff;
            color: #000000;
            border: 1px solid #ffffff;
        }

        section[data-testid="stSidebar"] .stButton button:hover,
        section[data-testid="stSidebar"] .stButton button:focus,
        section[data-testid="stSidebar"] .stButton button:active {
            background: #f5f5f5;
            color: #000000;
            border-color: #f5f5f5;
        }

        section[data-testid="stSidebar"] .stButton button p {
            color: #000000;
        }

        div[data-testid="stChatInput"] {
            background: #ffffff;
        }

        div[data-testid="stChatInput"] textarea {
            color: #000000;
        }
    </style>"""