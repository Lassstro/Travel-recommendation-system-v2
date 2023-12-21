from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
app = Flask(__name__)

dia_diem =  ["Đồi Thiên An – Hồ Thuỷ Tiên", "Núi Bạch Mã", "Chùa Huyền Không Sơn Thượng", "Biển Lăng Cô", "Biển Thuận An", "Khu nghỉ dưỡng Banyan Tree", "Khu nghỉ dưỡng Pilgrimage Village", "Chùa Thiên Mụ", "Chùa Từ Đàm", "Bảo tàng Mỹ thuật Cung đình Huế", "Thiền viện Trúc Lâm Bạch Mã", "Nhà vườn Huế", "Lăng tẩm Huế", "Cầu Tràng Tiền", "Đại Nội Huế", "Sông Hương", "Phá Tam Giang", "Phố đi bộ Huế", "Chợ Đông Ba", "Đèo Hải Vân"]

# Load mô hình đã được huấn luyện
loaded_model = joblib.load('Models/model.joblib')
loaded_encoder = joblib.load('Models/encoder.joblib')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    results = pd.DataFrame(columns=["Địa hình","Mức thu nhập", "Số lượng người", "Thời gian", "Mục đích du lịch","Địa điểm", "Đánh giá"])
    # Dự đoán trên dữ liệu mới
    for i in dia_diem:
        new_data = pd.DataFrame({
            'Địa hình': [request.json.get('terrain')],
            'Mức thu nhập': [request.json.get('income')],
            'Số lượng người': [request.json.get('numberOfPeople')],
            'Thời gian': [request.json.get('time')],
            'Mục đích du lịch': [request.json.get('purpose')],
            'Địa điểm': [i],
        })

        # Mã hóa dữ liệu mới
        new_data_encoded = loaded_encoder.transform(new_data)

        # Dự đoán trên dữ liệu mới
        new_predictions = loaded_model.predict(new_data_encoded)

        # In dự đoán
        new_data['Đánh giá'] = new_predictions[0]
        results = pd.concat([results, new_data], ignore_index=True)
    results = results.sort_values(by='Đánh giá', ascending=False)
    return jsonify(results.head(3).reset_index().to_dict())

if __name__ == '__main__':
    app.run(debug=True)
