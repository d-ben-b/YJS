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
              {{ edit_button_name }}
            </base-button>
            <base-button
              @click="deleteCourse(course.course_id)"
              :buttonType="button_type"
              :buttonBackground="true">
              {{ delete_button_name }}
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
    :allCourses="courses"
    :work_item_id="formData.work_item_id"
    @close="closeModal"
    @submit="handleModalSubmit" />
</template>

<script setup>
  import { useRoute } from "vue-router";
  import { ref, onMounted } from "vue";
  import axios from "axios";
  import CourseModal from "./CourseModal.vue";

  const courses = ref([]);
  const route = useRoute();
  const edit_button_name = ref("");
  const delete_button_name = ref("");
  const button_type = ref("");
  const showModal = ref(false);
  const isEditing = ref(false);
  const formData = ref({
    course_id: null,
    course_name: "",
    course_content: "",
    training_type_name: "",
    work_item_name: "",
    unit_name: "",
    department_name: "",
    evaluation_criteria: "",
    key_points: "",
    sop_sip: "",
    work_item_sop_img: [], // 已上傳的圖片
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
    isEditing.value = mode === "edit";
    formData.value = course
      ? { ...course }
      : {
          course_id: null,
          course_name: "",
          course_content: "",
          training_type_name: "",
          work_item_name: "",
          unit_name: "",
          department_name: "",
          evaluation_criteria: "",
          key_points: "",
          sop_sip: "",
          work_item_sop_img: [],
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
      const fileUploadFormData = new FormData(); // 使用 FormData 來支援檔案上傳

      // 添加可修改的欄位
      fileUploadFormData.append("course_name", data.course_name);
      fileUploadFormData.append("training_type_name", data.training_type_name);
      fileUploadFormData.append("work_item_name", data.work_item_name);
      fileUploadFormData.append("unit_name", data.unit_name);
      fileUploadFormData.append("department_name", data.department_name);
      fileUploadFormData.append(
        "evaluation_criteria",
        data.evaluation_criteria
      );
      fileUploadFormData.append("key_points", data.key_points);
      fileUploadFormData.append("sop_sip", data.sop_sip);

      // 添加上傳的檔案 (支援多個檔案)
      if (data.uploadedFiles && data.uploadedFiles.length > 0) {
        data.uploadedFiles.forEach((file, index) => {
          fileUploadFormData.append("uploadedFiles", file);
          console.log(`Appending file ${index + 1}:`, file);
        });
      } else {
        console.warn("沒有上傳的檔案");
      }

      // 調試 FormData 的內容
      for (let pair of fileUploadFormData.entries()) {
        console.log(`${pair[0]}: ${pair[1]}`);
      }

      // 發送請求
      const url = data.course_id
        ? `/api/courses/${data.course_id}`
        : "/api/courses";
      const method = data.course_id ? "put" : "post";

      await axios({
        method,
        url,
        data: fileUploadFormData,
        headers: { "Content-Type": "multipart/form-data" },
      });

      closeModal();
      getCourses(); // 重新加載課程列表
      alert("提交課程資料成功！");
    } catch (error) {
      console.error("提交表單失敗:", error);
      alert("提交課程資料失敗！");
    }
  };

  // 刪除課程
  const deleteCourse = async () => {
    if (button_type.value === "new") {
      alert("新增測驗題目");
      return;
    } else {
      try {
        await axios.delete(`/api/courses?course_id=${data.course_id}`);
        getCourses();
      } catch (error) {
        console.error("刪除課程失敗:", error);
        alert("刪除課程失敗！");
      }
    }
  };
  const button_name = () => {
    if (route.name === "course-table") {
      edit_button_name.value = "上傳/修改詳細資料";
      delete_button_name.value = "刪除";
      button_type.value = "delete";
    } else if (route.name === "course-table-view") {
      edit_button_name.value = "查看詳細資料";
      delete_button_name.value = "新增測驗題目";
      button_type.value = "new";
    } else {
      edit_button_name.value = "查看詳細資料";
      delete_button_name.value = "新增評核項目";
      button_type.value = "new";
    }
  };

  // 初始化
  onMounted(() => {
    getCourses();
    button_name();
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
