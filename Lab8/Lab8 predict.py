import cv2
import numpy as np
import ai_edge_litert.interpreter as tflite
import os

# 載入 TFLite 模型
interpreter = tflite.Interpreter(model_path="mnist_model.tflite")
interpreter.allocate_tensors()

# 取得輸入與輸出節點的詳細規格
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def preprocess_and_predict(image_path):
    # 影像預處理 (灰階 -> 二值化反轉 -> 自動裁切 -> 縮放)
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("無法讀取圖片")
        return

    # 用 OTSU 自動計算門檻，避免固定 127 導致太暗或太亮時失敗
    _, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        crop = thresh[y:y+h, x:x+w]
        
        # 建立全黑正方形畫布將數字置中，防止瘦長或寬扁的數字在縮放時拉伸變形
        max_side = max(w, h)
        pad = int(max_side * 0.25)  # 保持原邏輯比例的適當留白
        canvas_size = max_side + 2 * pad
        crop_padded = np.zeros((canvas_size, canvas_size), dtype=np.uint8)
        
        # 計算置中座標並將裁切數字貼上
        offset_y = pad + (max_side - h) // 2
        offset_x = pad + (max_side - w) // 2
        crop_padded[offset_y:offset_y+h, offset_x:offset_x+w] = crop
    else:
        crop_padded = thresh

    resized = cv2.resize(crop_padded, (28, 28), interpolation=cv2.INTER_AREA)

    # 資料標準化與形狀調整 (1, 28, 28, 1)
    normalized = resized.astype('float32') / 255.0
    final_input = np.expand_dims(normalized, axis=0)
    final_input = np.expand_dims(final_input, axis=-1)

    # 使用 TFLite 進行推論
    interpreter.set_tensor(input_details[0]['index'], final_input)
    interpreter.invoke()
    
    # 取得預測結果
    prediction = interpreter.get_tensor(output_details[0]['index'])
    result = np.argmax(prediction, axis=-1)[0]
    confidence = np.max(prediction)

    # 輸出帶有預測結果與信心度的照片
    # 先將 28x28 的二值化影像等比例放大到 280x280
    visual_img = cv2.resize(resized, (280, 280), interpolation=cv2.INTER_NEAREST)
    
    # 將灰階影像轉換為 BGR 彩色格式
    visual_img = cv2.cvtColor(visual_img, cv2.COLOR_GRAY2BGR)
    
    # 在上方外加一個高度 80 像素的獨立白色區塊（value=[255, 255, 255]）
    visual_img = cv2.copyMakeBorder(visual_img, 80, 0, 0, 0, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    
    # 在上方的白色區塊內繪製預測資訊
    cv2.putText(visual_img, f"Pred: {result}", (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(visual_img, f"Conf: {confidence*100:.1f}%", (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2, cv2.LINE_AA)
    
    # 儲存圖片
    file_name, _ = os.path.splitext(image_path)
    save_path = f"{file_name}_processed.png"
    cv2.imwrite(save_path, visual_img)
    print(f"預處理與標籤影像已儲存至 {save_path} (大小: 280x360)")

    print(f"辨識結果: {result} (信心度: {confidence*100:.2f}%)")

# 執行預測
preprocess_and_predict('image.jpg')