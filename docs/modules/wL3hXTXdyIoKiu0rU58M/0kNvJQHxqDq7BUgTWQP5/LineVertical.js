let Component;
let IconInner;
var Icon = (React) => {
  if (!Component) {
    Component = /* @__PURE__ */ new Map([
      [
        "bold",
        /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M140,24V232a12,12,0,0,1-24,0V24a12,12,0,0,1,24,0Z" }))
      ],
      [
        "duotone",
        /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(
          "path",
          {
            d: "M224,48V208a16,16,0,0,1-16,16H48a16,16,0,0,1-16-16V48A16,16,0,0,1,48,32H208A16,16,0,0,1,224,48Z",
            opacity: "0.2"
          }
        ), /* @__PURE__ */ React.createElement("path", { d: "M136,24V232a8,8,0,0,1-16,0V24a8,8,0,0,1,16,0Z" }))
      ],
      [
        "fill",
        /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M208,32H48A16,16,0,0,0,32,48V208a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V48A16,16,0,0,0,208,32ZM136,192a8,8,0,0,1-16,0V64a8,8,0,0,1,16,0Z" }))
      ],
      [
        "light",
        /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M134,24V232a6,6,0,0,1-12,0V24a6,6,0,0,1,12,0Z" }))
      ],
      [
        "regular",
        /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M136,24V232a8,8,0,0,1-16,0V24a8,8,0,0,1,16,0Z" }))
      ],
      [
        "thin",
        /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M132,24V232a4,4,0,0,1-8,0V24a4,4,0,0,1,8,0Z" }))
      ]
    ]);
    IconInner = React.forwardRef((props, ref) => /* @__PURE__ */ React.createElement("g", { ref, ...props }, Component.get(props.weight)));
  }
  return IconInner;
};
const __FramerMetadata__ = {
  exports: {
    default: {
      type: "reactComponent",
      slots: [],
      annotations: { framerContractVersion: "1" }
    },
    __FramerMetadata__: { type: "variable" }
  }
};
var LineVertical_default = Icon;
export {
  __FramerMetadata__,
  LineVertical_default as default
};
