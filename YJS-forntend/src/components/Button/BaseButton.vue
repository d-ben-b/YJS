<template>
  <button
    :class="['btn', buttonType, { disabled, buttonBackground }]"
    :disabled="disabled">
    <slot></slot>
  </button>
</template>

<script setup>
  const props = defineProps({
    buttonType: {
      type: String,
      default: "primary",
      validator: (value) =>
        ["primary", "new", "delete", "modify", "edit"].includes(value), // Ensures only valid types
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    buttonBackground: {
      type: Boolean,
      default: false,
    },
  });
</script>

<style scoped>
  .btn {
    color: black;
    font-family: "Inter", sans-serif;
    transition: transform 0.3s ease;
  }

  /* Primary Button Styles */
  .btn.primary {
    width: 255px;
    height: 67px;
    /* padding: 10px 20px; */
    border-radius: 20px;
    border: none;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.25);
    font-size: 22px;
    background-color: #757575;
    color: white;
  }

  /* New Button Styles */
  .btn.new {
    color: #32496e;
    font-size: 18px;
    font-weight: 700;
    line-height: 21.78px;
    text-align: center;
    text-decoration: none;
    height: 35px;
    border-radius: 10px;
    border: 2px solid #699ac7;
    opacity: 1; /* Ensure visibility */
    transition: background 0.3s ease;
    background: white;
  }

  /* Conditional Background for New Button */
  .btn.new.buttonBackground {
    background: #dfeaf4;
  }

  .btn.delete {
    color: #a90607;
    background: white;
    height: 35px;
    border-radius: 10px;
    border: 2px solid #df0f10;
    font-size: 18px;
    font-weight: 700;
    line-height: 21.78px;
    text-align: center;
    text-underline-position: from-font;
    text-decoration-skip-ink: none;
  }

  .btn.delete.buttonBackground {
    background: #ffcccb;
  }

  .btn.modify {
    padding: 0 12px 0;
    color: #666666;
    background: white;
    font-size: 18px;
    font-weight: 700;
    line-height: 21.78px;
    text-align: center;
    text-underline-position: from-font;
    text-decoration-skip-ink: none;
    height: 35px;
    border-radius: 10px;
    border: 2px solid #c6c6c6;
  }

  .btn.edit {
    font-size: 18px;
    font-weight: 700;
    line-height: 21.78px;
    text-align: center;
    text-underline-position: from-font;
    text-decoration-skip-ink: none;
    color: #7e5f05;
    background: #fff2cd;
    height: 35px;
    top: 685px;
    left: 1035px;
    gap: 0px;
    border-radius: 10px;
    border: 2px solid #f3c119;
  }
  /* Disabled Primary Button Styles */
  .btn.primary:disabled {
    opacity: 0.5;
    background-color: #d9d9d9;
    cursor: not-allowed;
    transform: none;
  }

  /* Hover Effects */
  .btn:hover {
    cursor: pointer;
    transform: scale(1.01);
  }

  .btn:disabled:hover {
    cursor: not-allowed;
    transform: none;
  }
</style>
