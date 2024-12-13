<template>
  <div class="course-table-container">
    <div class="header">
      <h2>課程管理</h2>
    </div>
    <!-- 課程列表 -->
    <table v-if="courses.length > 0" class="course-table">
      <thead>
        <tr>
          <th></th>
          <th>課程ID</th>
          <th>課程名稱</th>
          <th>教育訓練類型</th>
          <th>相關工作項目</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="course in courses" :key="course.course_id">
          <td><input type="checkbox" /></td>
          <td>{{ course.course_id }}</td>
          <td>{{ course.course_name }}</td>
          <td>{{ course.training_type_name }}</td>
          <td>{{ course.work_item_name }}</td>
          <td class="actions">
            <base-button
              @click="viewCourseDetail(course.course_id)"
              buttonType="modify">
              上傳/修改詳細資料
            </base-button>
            <base-button
              @click="deleteCourse(course.course_id)"
              buttonType="delete"
              :buttonBackground="true">
              刪除
            </base-button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- 新增課程按鈕 -->
    <div class="add-course-button">
      <base-button @click="openModal" buttonType="new">新增課程</base-button>
    </div>
  </div>
  <!-- 課程模組 -->
  <course-modal
    :show="showModal"
    :isEditing="isEditing"
    :formData="formData"
    @close="closeModal"
    @submit="handleModalSubmit" />
</template>

<script setup>
  import { ref, onMounted } from "vue";
  import axios from "axios";
  import CourseModal from "./CourseModal.vue";

  const courses = ref([]);
  const showModal = ref(false);
  const isEditing = ref(false);
  const formData = ref({
    course_id: null,
    course_name: "",
    course_date_start: "",
    course_date_end: "",
    course_time_start: "",
    course_time_end: "",
    course_content: "",
  });

  // 獲取課程資料
  const getCourses = async () => {
    try {
      const response = await axios.get("/api/courses");
      courses.value = response.data;
    } catch (error) {
      console.error("無法獲取課程資料:", error);
      alert("載入課程失敗！");
    }
  };

  // 開啟模組
  const openModal = (mode = "new", course = null) => {
    console.log("openModal", mode, course);
    isEditing.value = mode === "edit";
    formData.value = course
      ? { ...course }
      : {
          course_id: null,
          course_name: "",
          course_date_start: "",
          course_date_end: "",
          course_time_start: "",
          course_time_end: "",
          course_content: "",
        };
    showModal.value = true;
  };

  // 關閉模組
  const closeModal = () => {
    showModal.value = false;
  };

  // 查看課程詳細資料
  const viewCourseDetail = async (courseId) => {
    try {
      const response = await axios.get(`/api/courses?course_id=${courseId}`);
      openModal("edit", response.data);
    } catch (error) {
      console.error("無法獲取課程詳細資料:", error);
      alert("查看課程詳細資料失敗！");
    }
  };

  // 提交表單
  const handleModalSubmit = async (data) => {
    try {
      const url = data.course_id
        ? `/api/courses/${data.course_id}`
        : "/api/courses";
      const method = data.course_id ? "put" : "post";
      await axios({ method, url, data });
      closeModal();
      getCourses();
    } catch (error) {
      console.error("提交表單失敗:", error);
      alert("提交課程資料失敗！");
    }
  };

  // 刪除課程
  const deleteCourse = async (courseId) => {
    try {
      await axios.delete(`/api/courses/${courseId}`);
      getCourses();
    } catch (error) {
      console.error("刪除課程失敗:", error);
      alert("刪除課程失敗！");
    }
  };

  // 初始化
  onMounted(() => {
    getCourses();
  });
</script>

<style scoped>
  .course-table-container {
    margin: 20px;
  }

  .course-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
    font-size: 18px;
  }

  .course-table th,
  .course-table td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #ddd;
  }

  .course-table th {
    font-size: 18px;
    font-weight: 700;
    background-color: #f4f4f4;
  }

  .actions {
    display: flex;
    gap: 10px;
  }

  .add-course-button {
    margin-top: 20px;
  }
</style>
