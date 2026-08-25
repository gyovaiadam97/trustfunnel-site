let Component;
let IconInner;
var Icon = (React) => {
  if (!Component) {
    Component = /* @__PURE__ */ new Map([
      [
        "bold",
        /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M144,128a16,16,0,1,1-16-16A16,16,0,0,1,144,128Z" }))
      ],
      [
        "duotone",
        /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M176,128a48,48,0,1,1-48-48A48,48,0,0,1,176,128Z", opacity: "0.2" }), /* @__PURE__ */ React.createElement("path", { d: "M140,128a12,12,0,1,1-12-12A12,12,0,0,1,140,128Z" }))
      ],
      [
        "fill",
        /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M128,80a48,48,0,1,0,48,48A48,48,0,0,0,128,80Zm0,60a12,12,0,1,1,12-12A12,12,0,0,1,128,140Z" }))
      ],
      [
        "light",
        /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M138,128a10,10,0,1,1-10-10A10,10,0,0,1,138,128Z" }))
      ],
      [
        "regular",
        /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M140,128a12,12,0,1,1-12-12A12,12,0,0,1,140,128Z" }))
      ],
      [
        "thin",
        /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M136,128a8,8,0,1,1-8-8A8,8,0,0,1,136,128Z" }))
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
var Dot_default = Icon;
export {
  __FramerMetadata__,
  Dot_default as default
};
