<!-- @format -->

<template>
  <div class="container">
    <base-button buttonType="primary">課程內容準備</base-button>
    <base-button buttonType="primary">隨堂測驗內容準備</base-button>
    <base-button buttonType="primary">評量考核內容準備</base-button>
  </div>
</template>

<style>
  .container {
    width: 75%;
    margin-top: 80px;
    display: flex;
    justify-content: space-around; /* 均勻分佈按鈕，若要更多間距可以使用 space-evenly */
    align-items: center; /* 垂直居中對齊 */
    flex-wrap: wrap; /* 如果螢幕過小會自動換行 */
  }
</style>
