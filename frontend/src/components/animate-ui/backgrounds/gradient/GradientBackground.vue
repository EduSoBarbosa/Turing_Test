
<script setup lang="ts">
import {
  ReducedMotionConfig,
  useShouldReduceMotion,
} from "@animate-ui/vue/utils/motion";

import { usePageVisible } from "@animate-ui/vue/utils/use-page-visible";
import { cn } from "@/lib/utils";
import { motion, useInView } from "motion-v";
import { computed, shallowRef } from "vue";

defineOptions({ inheritAttrs: false });

const props = defineProps({
  class: {
    type: [Boolean, null, String, Object, Array],
    required: false,
    skipCheck: true,
  },
  transition: {
    type: Object,
    required: false,
    default: () => ({
      duration: 25,
      ease: "easeInOut",
      repeat: Infinity,
    }),
  },
});

const STATIC_POSITION = "0% 50%";

const element = shallowRef<HTMLElement | null>(null);

const inView = useInView(element);
const pageVisible = usePageVisible();
const reduce = useShouldReduceMotion();

const playing = computed(
  () => inView.value && pageVisible.value && !reduce.value,
);

const setElement = (node: any) => {
  const el = node?.$el ?? node;
  element.value = el instanceof HTMLElement ? el : null;
};

const gradientStyle = {
  backgroundImage: `
    linear-gradient(
      135deg,
      #171126 0%,
      #250B45 18%,
      #3900A8 35%,
      #6425D9 50%,
      #8B168F 65%,
      #3900A8 82%,
      #171126 100%
    )
  `,
};
</script>

<template>
  <ReducedMotionConfig>
    <motion.div
      :ref="setElement"
      data-slot="gradient-background"
      :class="
        cn(
          'size-full bg-size-[400%_400%]',
          props.class,
        )
      "
      :style="gradientStyle"
      :animate="{
        backgroundPosition: playing
          ? [STATIC_POSITION, '100% 50%', STATIC_POSITION]
          : STATIC_POSITION,
      }"
      :transition="playing ? transition : { duration: 0 }"
      v-bind="$attrs"
    >
      <slot />
    </motion.div>
  </ReducedMotionConfig>
</template>
