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
            <input
              type="text"
              v-model="localFormData.course_name"
              required
              :disabled="disabled" />
          </div>
          <div class="form-group">
            <label>教育訓練類型</label>
            <select
              v-model="localFormData.training_type_name"
              required
              :disabled="disabled">
              <option value="" disabled>選擇類型</option>
              <option
                v-for="(type, index) in trainingTypes"
                :key="index"
                :value="type">
                {{ type }}
              </option>
            </select>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>部門</label>
            <select
              v-model="localFormData.department_name"
              required
              :disabled="disabled">
              <option value="" disabled>選擇部門</option>
              <option v-for="(item, index) in department" :key="index">
                {{ item }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>單位</label>
            <select
              v-model="localFormData.unit_name"
              required
              :disabled="disabled">
              <option value="" disabled>選擇單位</option>
              <option v-for="(item, index) in unit" :key="index">
                {{ item }}
              </option>
            </select>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>工作項目</label>
            <select
              v-model="localFormData.work_item_name"
              required
              :disabled="disabled">
              <option value="" disabled>選擇項目</option>
              <option v-for="(item, work_id) in relateWorkItems" :key="work_id">
                {{ item }}
              </option>
            </select>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>SOP/SIP</label>
            <textarea
              v-model="localFormData.sop_sip"
              required
              :disabled="disabled"></textarea>
          </div>
          <div class="form-group">
            <div class="form-row">
              <div class="image-upload-container">
                <div
                  v-if="imageUrls.length > 0"
                  v-for="(url, index) in imageUrls"
                  :key="index"
                  class="image-preview">
                  <img :src="url" :alt="'圖片' + (index + 1)" />
                  <button
                    class="remove-btn"
                    @click.prevent="deleteServerImage(url, index)">
                    ✖
                  </button>
                </div>

                <div
                  v-if="localFormData.work_item_sop_img.length > 0"
                  v-for="(img, index) in localFormData.work_item_sop_img"
                  :key="index"
                  class="image-preview">
                  <img :src="img.previewUrl" :alt="'圖片' + (index + 1)" />
                  <button class="remove-btn" @click="removeImage(index)">
                    ✖
                  </button>
                </div>

                <div class="add-image" @click="triggerFileInput">
                  <br />
                  <span>+</span>
                  <p>新增圖片</p>
                  <input
                    type="file"
                    ref="fileInput"
                    accept="image/*"
                    @change="handleFileUpload"
                    multiple
                    style="display: none"
                    :disabled="disabled" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group full">
            <label>教學重點</label>
            <textarea
              v-model="localFormData.key_points"
              class="full"
              required
              :disabled="disabled"></textarea>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group full">
            <label>評量項目與標準</label>
            <textarea
              v-model="localFormData.evaluation_criteria"
              class="full"
              required
              :disabled="disabled"></textarea>
          </div>
        </div>

        <div class="form-actions">
          <base-button buttonType="modify" @click="$emit('close')"
            >取消</base-button
          >
          <base-button buttonType="edit" type="submit">{{
            isEditing ? "儲存" : "新增"
          }}</base-button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
  import { onMounted, ref, watch, onBeforeUnmount } from "vue";
  import axios from "axios";

  const props = defineProps({
    show: Boolean,
    isEditing: Boolean,
    formData: Object,
    allCourses: Array,
    work_item_id: Number,
  });

  const emit = defineEmits(["submit", "close"]);

  const disabled = !props.isEditing;
  const blobUrls = ref([]);
  const fileUploaded = ref([]);
  const trainingTypes = ref([]);
  const relateWorkItems = ref([]);
  const unit = ref([]);
  const department = ref([]);
  const fileInput = ref(null);
  const imageUrls = ref([]);

  function hexToBlob(hex, mimeType = "image/jpeg") {
    const byteArray = new Uint8Array(
      hex.match(/.{1,2}/g).map((byte) => parseInt(byte, 16))
    );
    return new Blob([byteArray], { type: mimeType });
  }

  function getImagePreview(hexString) {
    const blob = hexToBlob(hexString, "image/jpeg");
    const url = URL.createObjectURL(blob);
    blobUrls.value.push(url);
    return url;
  }

  function cleanUpBlobUrls() {
    blobUrls.value.forEach((url) => URL.revokeObjectURL(url));
    blobUrls.value = [];
  }

  const localFormData = ref({
    ...props.formData,
    work_item_sop_img: Array.isArray(props.formData.work_item_sop_img)
      ? props.formData.work_item_sop_img.map((hex) => ({
          previewUrl: getImagePreview(hex),
          hex,
        }))
      : [],
  });

  const getImages = async (ID) => {
    if (ID) {
      const response = await axios.get(
        `/api/work_item_images?work_item_id=${ID}`
      );
      if (response.data && response.data.images) {
        imageUrls.value = response.data.images;
      }
    }
  };

  watch(
    () => props.formData,
    (newVal) => {
      cleanUpBlobUrls();
      getImages(newVal.work_item_id);

      if (
        Array.isArray(newVal.work_item_sop_img) &&
        newVal.work_item_sop_img.length > 0
      ) {
        localFormData.value = {
          ...newVal,
          work_item_sop_img: newVal.work_item_sop_img.map((hex) => ({
            previewUrl: getImagePreview(hex),
            hex,
          })),
        };
        fileUploaded.value = [...localFormData.value.work_item_sop_img];
      } else {
        localFormData.value = {
          ...newVal,
          work_item_sop_img: [],
        };
        fileUploaded.value = [];
      }
    },
    { immediate: true }
  );

  const handleFileUpload = async (event) => {
    const files = Array.from(event.target.files);
    const maxFileSize = 5 * 1024 * 1024;

    for (const file of files) {
      if (file.size > maxFileSize) {
        alert("檔案大小超過 5MB！");
        continue;
      }

      const previewUrl = URL.createObjectURL(file);
      blobUrls.value.push(previewUrl);

      try {
        const hexString = await fileToHex(file);
        const newImg = { previewUrl, hex: hexString, file };
        localFormData.value.work_item_sop_img.push(newImg);
        fileUploaded.value.push(newImg);
      } catch (error) {
        alert("上传图片时发生错误，请重试。");
      }
    }

    event.target.value = null;
  };

  function fileToHex(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        const arrayBuffer = reader.result;
        const byteArray = new Uint8Array(arrayBuffer);
        const hexString = Array.from(byteArray)
          .map((byte) => byte.toString(16).padStart(2, "0"))
          .join("");
        resolve(hexString);
      };
      reader.onerror = () => {
        reject(new Error("文件讀取失敗"));
      };
      reader.readAsArrayBuffer(file);
    });
  }

  function removeImage(index) {
    const imgObj = localFormData.value.work_item_sop_img[index];
    if (imgObj && imgObj.previewUrl.startsWith("blob:")) {
      URL.revokeObjectURL(imgObj.previewUrl);
      blobUrls.value = blobUrls.value.filter(
        (blobUrl) => blobUrl !== imgObj.previewUrl
      );
    }

    localFormData.value.work_item_sop_img.splice(index, 1);
    fileUploaded.value.splice(index, 1);
  }

  function triggerFileInput() {
    fileInput.value.click();
  }

  const submitForm = async () => {
    const data = { ...localFormData.value };
    if (Array.isArray(data.work_item_sop_img)) {
      data.work_item_sop_img = data.work_item_sop_img.map(
        (imgObj) => imgObj.hex
      );
    }
    data.uploadedFiles = fileUploaded.value.map((imgObj) => imgObj.file);
    emit("submit", data);
  };

  const findTrainingTypes = async () => {
    const response = await fetchUniqueValues();
    trainingTypes.value = response.training_type_name || [];
    relateWorkItems.value = response.work_item_name || [];
    unit.value = response.unit_name || [];
    department.value = response.department_name || [];
  };

  async function fetchUniqueValues() {
    try {
      const response = await axios.get(
        `/api/all_values?fields=training_type_name,work_item_name,unit_name,department_name`
      );
      return response.data;
    } catch (error) {
      return {};
    }
  }

  const deleteServerImage = async (imageUrl, index) => {
    try {
      const urlObj = new URL(imageUrl, window.location.origin);
      const imageId = urlObj.searchParams.get("id");
      await axios.delete(`/api/work_item_image?id=${imageId}`);
      imageUrls.value.splice(index, 1);
      alert("圖片刪除成功！");
    } catch (error) {
      alert("刪除圖片失敗！");
    }
  };

  onBeforeUnmount(() => {
    cleanUpBlobUrls();
  });

  onMounted(() => {
    findTrainingTypes();
    getImages(props.work_item_id);
  });
</script>

<style scoped>
  .full {
    width: 100%;
  }
  .start {
    justify-content: flex-start !important;
  }
  .grow {
    flex-grow: 1;
  }
  .modal-overlay {
    position: fixed;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }

  .modal {
    background: #fff;
    padding: 20px 39px;
    width: 707px;
    max-height: 90vh;
    overflow-y: auto;
    border-radius: 31px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  }

  .modal-header {
    color: #666666;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 22px;
  }

  .modal-header h3 {
    font-size: 20px;
    font-weight: 700;
    margin: 0;
  }

  .close-btn {
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
  }

  .form-group {
    align-items: center;
    display: flex;
    flex-direction: row;
    margin-bottom: 15px;
  }

  .form-group label {
    width: 100px;
    font-weight: bold;
    margin-bottom: 5px;
  }

  input {
    width: 184px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    resize: none;
  }
  select {
    width: 154px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    resize: none;
  }

  .form-row {
    display: flex;
    gap: 20px;
    justify-content: flex-start;
    margin-bottom: 10px;
    width: 100%;
  }

  .form-actions {
    display: flex;
    justify-content: flex-start;
    gap: 10px;
    margin-top: 20px;
  }

  .edit-button {
    padding: 10px 20px;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }

  .delete-button {
    padding: 10px 20px;
    background-color: #f44336;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }

  .image-upload-container {
    display: flex;
    gap: 10px;
    align-items: center;
    justify-self: center;
    flex-wrap: wrap;
  }

  .image-preview {
    position: relative;
    width: 74px;
    height: 58px;
    border: 1px solid #ccc;
    border-radius: 4px;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .image-preview img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .remove-btn {
    position: absolute;
    top: 2px;
    right: 2px;
    background: rgba(0, 0, 0, 0.5);
    color: white;
    border: none;
    border-radius: 50%;
    font-size: 12px;
    width: 18px;
    height: 18px;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
  }

  .add-image {
    width: 74px;
    height: 58px;
    border: 1px dashed #ccc;
    border-radius: 4px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: #666;
    cursor: pointer;
    font-size: 14px;
  }

  .add-image span {
    font-size: 20px;
    font-weight: bold;
  }

  .add-image p {
    margin-top: 0;
  }

  .add-image:hover {
    background-color: #f9f9f9;
  }

  .full {
    width: 100%;
    height: 100px;
  }

  textarea {
    height: 50px;
    resize: none;
  }
</style>
