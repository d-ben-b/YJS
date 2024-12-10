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
          <td>{{ course.training_type }}</td>
          <td>{{ course.related_project }}</td>
          <td class="actions">
            <base-button
              v-if="showModify"
              @click="viewCourseDetail(course.course_id)"
              buttonType="modify">
              {{ buttonEditName }}
            </base-button>
            <base-button
              v-if="showDelete"
              @click="deleteCourse(course.course_id)"
              buttonType="delete"
              :buttonBackground="true">
              刪除
            </base-button>
            <base-button
              v-if="showNew"
              @click="addQuiz(course.course_id)"
              buttonType="new"
              :buttonBackground="true">
              {{ buttonNewName }}
            </base-button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- 新增課程按鈕 -->
    <div class="add-course-button">
      <base-button @click="toggleForm" buttonType="new">新增課程</base-button>
    </div>

    <!-- 課程表單 -->
    <form v-if="showForm" @submit.prevent="submitCourse" class="course-form">
      <h3>{{ isEditing ? "編輯課程" : "新增課程" }}</h3>
      <label for="course_name">課程名稱:</label>
      <input type="text" v-model="formData.course_name" required />

      <label for="course_date_start">開始日期:</label>
      <input type="date" v-model="formData.course_date_start" required />

      <label for="course_date_end">結束日期:</label>
      <input type="date" v-model="formData.course_date_end" required />

      <label for="course_time_start">開始時間:</label>
      <input type="time" v-model="formData.course_time_start" required />

      <label for="course_time_end">結束時間:</label>
      <input type="time" v-model="formData.course_time_end" required />

      <label for="course_content">課程內容:</label>
      <textarea v-model="formData.course_content" required></textarea>

      <div class="form-actions">
        <base-button type="submit" buttonType="edit">
          {{ isEditing ? "儲存" : "新增課程" }}
        </base-button>
        <base-button @click="cancelForm" buttonType="modify">取消</base-button>
      </div>
    </form>
  </div>
</template>

<script setup>
  import { ref, onMounted } from "vue";
  import { useRouter } from "vue-router";
  import axios from "axios";

  const router = useRouter();
  const showModify = ref(true); // 保留
  const showDelete = ref(true); // 保留
  const showNew = ref(true); // 保留
  const showForm = ref(false);
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
  const courses = ref([]);
  var buttonEditName = ""; // 保留不變
  var buttonNewName = ""; // 保留不變

  // 讀取課程資料
  const getCourses = async () => {
    try {
      const response = await axios.get("/api/courses");
      courses.value = response.data;
    } catch (error) {
      console.error("Error fetching courses", error);
    }
  };

  // 按鈕初始化
  const button = () => {
    const routerName = router.currentRoute.value.name;
    console.log(routerName);
    if (routerName === "course-table") {
      buttonEditName = "上傳/修改詳細資料";
      showNew.value = false;
    } else if (
      routerName === "course-table-view" ||
      routerName === "course-table-list"
    ) {
      buttonEditName = "查看詳細資料";
      buttonNewName =
        routerName === "course-table-view" ? "新增測驗題目" : "新增評核項目";
      showDelete.value = false;
    } else {
      buttonEditName = "error";
    }
  };

  // 切換新增/編輯課程表單
  const toggleForm = () => {
    showForm.value = !showForm.value;
    if (!showForm.value) {
      resetForm();
    }
  };

  // 初始化表單資料
  const resetForm = () => {
    formData.value = {
      course_id: null,
      course_name: "",
      course_date_start: "",
      course_date_end: "",
      course_time_start: "",
      course_time_end: "",
      course_content: "",
    };
    isEditing.value = false;
  };

  // 提交表單（新增或編輯）
  const submitCourse = async () => {
    try {
      if (isEditing.value) {
        await axios.put(
          `/api/courses/${formData.value.course_id}`,
          formData.value
        );
      } else {
        await axios.post("/api/courses", formData.value);
      }
      showForm.value = false;
      getCourses();
    } catch (error) {
      console.error("Error submitting course", error);
    }
  };

  // 刪除課程
  const deleteCourse = async (courseId) => {
    try {
      await axios.delete(`/api/courses/${courseId}`);
      getCourses();
    } catch (error) {
      console.error("Error deleting course", error);
    }
  };

  // 查看課程詳細資料
  const viewCourseDetail = async (courseId) => {
    try {
      const response = await axios.get(`/api/courses/${courseId}`);
      console.log("課程詳細資料:", response.data);
    } catch (error) {
      console.error("Error fetching course detail", error);
    }
  };

  // 初始化
  onMounted(() => {
    getCourses();
    button();
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
    font-size: 14px;
  }

  .course-table th,
  .course-table td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #ffffff;
  }

  .course-table th {
    background-color: #f4f4f4;
    font-weight: bold;
  }

  .course-table .actions {
    display: flex;
    gap: 10px;
  }

  .add-course-button {
    margin-top: 20px;
  }

  .course-form {
    margin-top: 20px;
    display: flex;
    flex-direction: column;
  }

  .course-form label {
    margin: 10px 0 5px;
  }

  .course-form input,
  .course-form textarea {
    width: 100%;
    padding: 10px;
    margin-bottom: 15px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }

  .form-actions {
    display: flex;
    justify-content: space-between;
  }
</style>
