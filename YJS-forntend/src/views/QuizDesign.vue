<template>
  <RightSideBar @select-item="handleSelectItem" />
  <div class="quiz-design">
    <!-- 動態路徑顯示 -->
    <div class="breadcrumb">
      {{ breadcrumb }}
    </div>

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

    <!-- 圖片選項部分 -->
    <div class="section">
      <h3>選擇題</h3>
      <div class="quiz-list">
        <div v-if="router_name === 'quiz-design-review'">
          <div
            v-for="(quizItem, index) in choiceQuizzes"
            :key="index"
            class="quiz-item">
            <div class="review-section">
              <label>
                <input
                  type="radio"
                  :name="'status-' + index"
                  value="通過/採用"
                  v-model="quizItem.status"
                  :aria-checked="quizItem.status === '通過/採用'"
                  @change="updateStatus(quizItem)" />
                通過/採用
              </label>
              <label>
                <input
                  type="radio"
                  :name="'status-' + index"
                  value="通過/保留"
                  v-model="quizItem.status"
                  :aria-checked="quizItem.status === '通過/保留'"
                  @change="updateStatus(quizItem)" />
                通過/保留
              </label>
              <label>
                <input
                  type="radio"
                  :name="'status-' + index"
                  value="不通過"
                  v-model="quizItem.status"
                  :aria-checked="quizItem.status === '不通過'" />
                不通過
              </label>
              <div v-if="quizItem.status === '不通過'">
                <label>原因：</label>
              </div>
              <div v-if="quizItem.status === '不通過'">
                <input
                  type="text"
                  v-model="quizItem.reason"
                  placeholder="輸入完按 Enter 鍵保存"
                  required
                  @change="updateStatus(quizItem)" />
              </div>
            </div>

            <p><strong>題目：</strong> {{ quizItem.name }}</p>
            <ul class="options">
              <li
                v-for="(option, optIndex) in quizItem.options"
                :key="optIndex">
                <input type="radio" v-model="quizItem.reason" />
                {{ option }}
              </li>
            </ul>
          </div>
        </div>
      </div>
      <div class="new-quiz">
        <input
          type="text"
          v-model="newChoiceQuiz.question"
          placeholder="輸入題目"
          class="quiz-input" />
        <div
          v-for="(option, index) in newChoiceQuiz.options"
          :key="index"
          class="option-item">
          <input
            type="text"
            v-model="option.text"
            placeholder="輸入選項"
            class="option-input" />
          <BaseButton
            buttonType="delete"
            @click="removeOption(index)"
            class="delete">
            刪除選項
          </BaseButton>
        </div>
        <BaseButton buttonType="new" @click="addOption">新增選項</BaseButton>
        <BaseButton
          buttonType="new"
          :buttonBackground="true"
          @click="saveChoiceQuiz('choice')">
          新增選擇題
        </BaseButton>
      </div>
    </div>

    <div class="section">
      <h3>問答題</h3>
      <div v-if="router_name === 'quiz-design-review'"></div>
      <div class="quiz-list">
        <div
          v-for="(quizItem, index) in questionQuizzes"
          :key="index"
          class="quiz-item">
          <p><strong>題目：</strong> {{ quizItem.name }}</p>
          <p><strong>答案：</strong> {{ quizItem.answer }}</p>
        </div>
      </div>
      <div class="new-quiz">
        <input
          type="text"
          v-model="newQuestionQuiz.question"
          placeholder="輸入題目"
          class="quiz-input" />
        <input
          type="text"
          v-model="newQuestionQuiz.answer"
          placeholder="輸入參考解答"
          class="quiz-input" />
        <BaseButton
          buttonType="new"
          :buttonBackground="true"
          @click="saveChoiceQuiz('question')">
          新增選擇題
        </BaseButton>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref } from "vue";
  import axios from "axios";
  import { useRouter } from "vue-router";
  import BaseButton from "@/components/Button/BaseButton.vue";
  import RightSideBar from "@/components/RightSideBar.vue";

  const router = useRouter();
  const router_name = router.currentRoute.value.name;
  // 表單數據
  const quiz = ref({
    sop: "",
    keyPoints: "",
    evaluation: "",
    type: "",
  });

  const newChoiceQuiz = ref({
    question: "",
    options: [{ text: "" }],
  });
  const newQuestionQuiz = ref({
    question: "",
    answer: "",
  });

  const images = ref([]);
  const quizzes = ref([]);
  const choiceQuizzes = ref([]);
  const questionQuizzes = ref([]);
  const currentWorkItemId = ref(0);

  // 動態路徑顯示
  const breadcrumb = ref("部門 > 單位 > 工作項目");

  const addOption = () => {
    newChoiceQuiz.value.options.push({ text: "" });
  };

  const removeOption = (index) => {
    newChoiceQuiz.value.options.splice(index, 1);
  };

  const saveChoiceQuiz = async (type) => {
    var submitData = null;
    if (type === "choice") {
      if (!newChoiceQuiz.value.question.trim()) {
        alert("請輸入題目");
        return;
      }

      if (
        type === "choice" &&
        newChoiceQuiz.value.options.some((option) => !option.text.trim())
      ) {
        alert("請輸入所有選項");
        return;
      }
    } else {
      if (!newQuestionQuiz.value.question.trim()) {
        alert("請輸入題目");
        return;
      }
    }

    submitData = type === "choice" ? newChoiceQuiz : newQuestionQuiz;

    try {
      const response = await axios.post("/api/quizzes", {
        work_item_id: currentWorkItemId.value,
        name: submitData.value.question,
        type: type,
        options:
          type === "choice"
            ? submitData.value.options.map((option) => option.text)
            : [],
        answer: type === "question" ? submitData.value.answer : null,
      });

      alert("選擇題新增成功！");
      await fetchQuizzesByWorkItem(currentWorkItemId.value);
      submitData.value = {
        question: "",
        options: [{ text: "" }],
      };
    } catch (error) {
      console.error("新增選擇題失敗：", error);
      alert("無法新增選擇題，請稍後再試。");
    }
  };

  // 當選擇工作項目時的處理函數
  const handleSelectItem = async (workItemId, pathArray) => {
    try {
      // 確保只有有效的 workItemId 時進行請求
      if (!workItemId) return;

      currentWorkItemId.value = workItemId;

      // 更新路徑顯示
      breadcrumb.value = pathArray.join(" > ");

      // 請求後端 API 獲取數據
      const response = await axios.get(`/api/work_items/${workItemId}`);
      const data = response.data;

      quiz.value.sop = data.sop_sip || "";
      quiz.value.keyPoints = data.key_points || "";
      quiz.value.evaluation = data.evaluation_criteria || "";
      images.value = (data.images || []).map((image) => ({
        url: `data:image/png;base64,${image}`,
      }));

      // 獲取與 work_item_id 對應的 Quiz
      await fetchQuizzesByWorkItem(workItemId);
    } catch (err) {
      console.error("Error loading work item data:", err);
      alert("Error loading data. Please try again.");
    }
  };

  // 上傳圖片
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

  const fetchQuizzesByWorkItem = async (workItemId) => {
    try {
      const response = await axios.get("/api/quizzes", {
        params: { work_item_id: workItemId },
      });

      quizzes.value = response.data;
      choiceQuizzes.value = quizzes.value.filter(
        (quiz) => quiz.type === "choice" && quiz.options !== null
      );
      questionQuizzes.value = quizzes.value.filter(
        (quiz) => quiz.type === "question" && quiz.answer !== null
      );
    } catch (error) {
      console.error("無法加載 Quiz 資料：", error);
    }
  };

  const updateStatus = async (quizItem) => {
    console.log("Selected status:", quizItem.status);

    try {
      if (quizItem.status === "不通過" && !quizItem.reason) {
        alert("請輸入原因！");
        return;
      }
      await axios.put(`/api/quiz/${quizItem.id}`, {
        options: quizItem.options,
        status: quizItem.status,
        reason: quizItem.reason || null,
      });
      alert("狀態更新成功！");
    } catch (error) {
      console.error("狀態更新失敗：", error);
      alert("更新失敗，請稍後再試！");
    }
  };
</script>

<style scoped>
  .quiz-design {
    width: 100%;
    max-width: 800px;
    margin: 0 auto;
    font-family: Arial, sans-serif;
  }

  .breadcrumb {
    color: #666666;
    font-family: Inter;
    font-size: 20px;
    font-weight: 700;
    line-height: 24.2px;
    text-align: left;
    text-underline-position: from-font;
    text-decoration-skip-ink: none;
  }

  .quiz-design .section {
    margin-bottom: 20px;
  }

  .quiz-design .section h3 {
    line-height: 45px;
    /* 與高度一致 */
    width: 100%;
    height: 45px;
    border: 2px solid #e4e4e4;
    background: #f5f5f5;
    padding-left: 10px;
    margin: 0;
    font-size: 18px;
    font-weight: 700;
    box-sizing: border-box;
    /* 確保邊框和內邊距一起計算 */
  }

  .quiz-design textarea {
    width: 100%;
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 10px;
    font-size: 14px;
    box-sizing: border-box;
  }

  .quiz-design .image-upload {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 10px;
  }

  .quiz-design .image-container {
    position: relative;
    display: inline-block;
  }

  .quiz-design .image-container img {
    width: 100px;
    height: 100px;
    object-fit: cover;
    border: 1px solid #ddd;
    border-radius: 4px;
  }

  .quiz-design .upload-button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100px;
    height: 100px;
    border: 1px dashed #aaa;
    border-radius: 4px;
    cursor: pointer;
  }

  .quiz-design .upload-button input {
    display: none;
  }

  .quiz-design .option-item {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
  }

  .quiz-design .option-item input {
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 5px;
    font-size: 14px;
    border: 2px solid #c6c6c6;
    width: 150px;
    height: 35px;
    top: 354px;
    box-sizing: border-box;
  }

  .quiz-design .add-option-button,
  .quiz-design .remove-button {
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 5px 10px;
    cursor: pointer;
    font-size: 14px;
  }

  .quiz-design .remove-button {
    background-color: #d9534f;
  }

  .quiz-design .submit-button {
    width: 100%;
    padding: 10px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 16px;
    cursor: pointer;
  }

  .quiz-design .submit-button:hover {
    background-color: #0056b3;
  }

  .quiz-list {
    margin-bottom: 20px;
  }

  .quiz-item {
    border: 1px solid #ddd;
    padding: 10px;
    margin-bottom: 10px;
  }
  .quiz-item .options {
    display: flex;
    list-style-type: none;
  }

  .new-quiz {
    margin-bottom: 20px;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #f9f9f9;
  }

  .quiz-input,
  .option-input {
    width: 625px;
    height: 35px;
    margin-bottom: 10px;
    padding: 8px;
    border: 2px solid #c6c6c6;
    border-radius: 4px;
    font-size: 14px;
    box-sizing: border-box;
  }

  .add-option-button,
  .remove-option-button,
  .save-quiz-button {
    padding: 8px 12px;
    font-size: 14px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  .delete {
    font-size: 18px;
    font-weight: 700;
    line-height: 21.78px;
    text-align: center;
    text-underline-position: from-font;
    text-decoration-skip-ink: none;
    width: 129px;
    height: 35px;
    border: 2px solid #df0f10;
  }

  .save-quiz-button {
    background-color: #28a745;
    color: white;
    margin-top: 10px;
  }

  .review-section {
    display: flex;
    margin: 20px 0;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #f9f9f9;
  }

  .review-section label {
    display: block;
    margin-bottom: 10px;
    font-size: 16px;
  }

  .review-section input[type="text"] {
    max-width: 400px;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
</style>
