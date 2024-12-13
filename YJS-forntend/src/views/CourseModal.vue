<template>
  <div class="modal-overlay" v-if="show">
    <div class="modal">
      <div class="modal-header">
        <h3>{{ isEditing ? "編輯課程" : "新增課程" }}</h3>
        <button class="close-btn" @click="$emit('close')">✖</button>
      </div>
      <form @submit.prevent="submitForm">
        <div class="form-row">
          <div class="form-group">
            <label>課程名稱</label>
            <input type="text" v-model="localFormData.course_name" required />
          </div>

          <div class="form-group">
            <label>教育訓練類型</label>
            <select v-model="localFormData.training_type">
              <option value="" disabled>選擇類型</option>
              <option value="type1">類型1</option>
              <option value="type2">類型2</option>
            </select>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>部門</label>
            <select v-model="localFormData.department">
              <option value="" disabled>選擇部門</option>
              <option value="dept1">部門1</option>
              <option value="dept2">部門2</option>
            </select>
          </div>
          <div class="form-group">
            <label>單位</label>
            <select v-model="localFormData.department">
              <option value="" disabled>選擇單位</option>
              <option value="dept1">單位1</option>
              <option value="dept2">單位2</option>
            </select>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>相關工作項目</label>
            <select v-model="localFormData.work_item">
              <option value="" disabled>選擇項目</option>
              <option value="item1">項目1</option>
              <option value="item2">項目2</option>
            </select>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>SOP/SIP</label>
            <textarea v-model="localFormData.sop_sip"></textarea>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group full">
            <label>教學重點</label>
            <textarea
              v-model="localFormData.key_points"
              class="full"></textarea>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group full">
            <label>評量項目與標準</label>
            <textarea
              v-model="localFormData.evaluation_criteria"
              class="full"></textarea>
          </div>
        </div>

        <div class="form-actions">
          <base-button buttonType="edit">
            {{ isEditing ? "儲存" : "新增" }}
          </base-button>
          <base-button
            buttonType="delete"
            @click="$emit('close')"
            :buttonBackground="true">
            取消</base-button
          >
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
  import { ref, watch } from "vue";

  const props = defineProps(["show", "isEditing", "formData"]);
  const localFormData = ref({ ...props.formData });

  watch(
    () => props.formData,
    (newVal) => {
      localFormData.value = { ...newVal };
    }
  );

  const submitForm = () => {
    const data = { ...localFormData.value };
    emit("submit", data);
  };
</script>

<style scoped>
  .full {
    width: 100%;
    height: 65px;
  }
  .modal-overlay {
    position: fixed;
    width: 100%;
    height: 100%;
    top: 70px;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    z-index: 1000;
  }

  .modal {
    position: relative;
    background: #fff;
    padding: 20px 18px;
    width: 737px;
    height: 567px;
    top: 109px;
    left: 160px;
    border-radius: 31px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  }

  .modal-header {
    color: #666666;
    height: 28px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 22px;
  }
  .modal-header h3 {
    font-size: 20px;
    font-weight: 700;
    line-height: 24.2px;
    text-align: left;
    text-underline-position: from-font;
    text-decoration-skip-ink: none;
    margin: 0;
  }

  .close-btn {
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
  }

  .form-group {
    display: flex;
    flex-wrap: nowrap;
    margin-bottom: 15px;
    align-items: center;
  }

  .form-group label {
    width: 100px;
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
    margin-right: 10px;
  }

  input,
  textarea,
  select {
    width: 184px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    resize: none;
  }
  .form-row {
    display: flex;
    gap: 20px;
    justify-content: space-between;
    margin-bottom: 10px;
  }

  .form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
  }

  .save-btn,
  .cancel-btn {
    padding: 10px 15px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }

  .save-btn {
    background-color: #4caf50;
    color: white;
  }

  .cancel-btn {
    background-color: #f44336;
    color: white;
  }
</style>
