<template>
  <RightSideBar />
  <div class="quiz-design">
    <h2>SOP/SIP 設計</h2>

    <!-- SOP/SIP -->
    <div class="section">
      <h3>SOP/SIP</h3>
      <textarea
        v-model="quiz.sop"
        placeholder="輸入 SOP/SIP..."
        rows="4"></textarea>
      <div class="image-upload">
        <div
          v-for="(image, index) in images"
          :key="index"
          class="image-container">
          <img :src="image.url" alt="Uploaded Image" />
          <button @click="removeImage(index)">×</button>
        </div>
        <label class="upload-button">
          <input type="file" accept="image/*" @change="handleImageUpload" />
          +
        </label>
      </div>
    </div>

    <!-- 教學重點 -->
    <div class="section">
      <h3>教學重點</h3>
      <textarea
        v-model="quiz.keyPoints"
        placeholder="輸入教學重點..."
        rows="4"></textarea>
    </div>

    <!-- 評量項目與標準 -->
    <div class="section">
      <h3>評量項目與標準</h3>
      <textarea
        v-model="quiz.evaluation"
        placeholder="輸入評量項目與標準..."
        rows="4"></textarea>
    </div>

    <!-- 提交按鈕 -->
    <button class="submit-button" @click="submitQuiz">提交</button>
  </div>
</template>

<script setup>
  import { ref, onMounted } from "vue";
  import RightSideBar from "@/components/RightSideBar.vue";

  const quiz = ref({
    sop: "",
    keyPoints: "",
    evaluation: "",
  });

  const images = ref([]);
  const first_time_view = ref(true);

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        images.value.push({ url: e.target.result });
      };
      reader.readAsDataURL(file);
    }
  };

  const removeImage = (index) => {
    images.value.splice(index, 1);
  };

  const submitQuiz = () => {
    console.log("提交的資料:", {
      sop: quiz.value.sop,
      keyPoints: quiz.value.keyPoints,
      evaluation: quiz.value.evaluation,
      images: images.value,
    });
    alert("資料已提交！");
  };
</script>

<style scoped>
  .quiz-design {
    width: 100%;
    max-width: 800px;
    margin: 0 auto;
    font-family: Arial, sans-serif;
  }

  .section {
    margin-bottom: 20px;
  }

  textarea {
    width: 100%;
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 10px;
    font-size: 14px;
  }

  .image-upload {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 10px;
  }

  .image-container {
    position: relative;
    display: inline-block;
  }

  .image-container img {
    width: 100px;
    height: 100px;
    object-fit: cover;
    border: 1px solid #ddd;
    border-radius: 4px;
  }

  .image-container button {
    position: absolute;
    top: 5px;
    right: 5px;
    background-color: red;
    color: white;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    font-size: 14px;
    padding: 5px;
  }

  .upload-button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100px;
    height: 100px;
    border: 1px dashed #aaa;
    border-radius: 4px;
    cursor: pointer;
  }

  .upload-button input {
    display: none;
  }

  .submit-button {
    width: 100%;
    padding: 10px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 16px;
    cursor: pointer;
  }

  .submit-button:hover {
    background-color: #0056b3;
  }
</style>
