<!-- @format -->

<template>
  <button :class="['btn', buttonType]" :disabled="disabled">
    <slot></slot>
  </button>
</template>

<script>
  export default {
    props: {
      buttonType: {
        type: String,
        default: "primary",
      },
      disabled: {
        type: Boolean,
        default: false,
      },
    },
  };
</script>

<style scoped>
  .btn {
    width: 255px;
    height: 67px;
    padding: 10px 20px;
    border-radius: 20px;
    border: none;
    box-shadow: 0px 4px 6px #00000040;
    font-size: 22px;
    font-family: Inter;
  }

  .btn.primary {
    background-color: #757575;
    color: white;
  }

  .btn.secondary {
    background-color: #6c757d;
    color: white;
  }

  .btn:disabled {
    opacity: 0.5;
  }
</style>
