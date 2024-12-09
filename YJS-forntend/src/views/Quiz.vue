<template>
  <div class="container">
    <base-button buttonType="primary">查看課程詳細資料</base-button>
    <base-button buttonType="primary">評量考核題目設計</base-button>
    <base-button buttonType="primary">評量考核表規劃與審核</base-button>
    <base-button buttonType="primary" :disabled="true" class="margin"
      >評量表規劃</base-button
    >
    <base-button buttonType="primary" :disabled="true" class="margin"
      >評量表審核</base-button
    >
  </div>
</template>

<style scoped>
  .container button {
    margin-right: 22px;
  }
  .margin {
    margin-top: 23px;
  }
</style>
