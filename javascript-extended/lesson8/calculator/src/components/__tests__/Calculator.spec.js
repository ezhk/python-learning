import {mount} from '@vue/test-utils';
import Calculator from '@/components/Calculator';


describe('Basic operations, operands: 52 and 4', () => {
  const wrapper = mount(Calculator);
  wrapper.vm.resetInitData();

  wrapper.setData({
    leftOperand: 52,
    inputValue: 4,
  });

  it('add operation', () => {
    expect(wrapper.vm.add()).toBe(56)
  });
  it('sub operation', () => {
    expect(wrapper.vm.sub()).toBe(48)
  });
  it('mul operation', () => {
    expect(wrapper.vm.mul()).toBe(208)
  });
  it('div operation', () => {
    expect(wrapper.vm.div()).toBe(13)
  });
});

describe('Div to zero: "100 and "0"', () => {
  const wrapper = mount(Calculator);
  wrapper.vm.resetInitData();

  wrapper.setData({
    leftOperand: 100,
    inputValue: 0,
  });
  it('result must be Infinity', () => {
    expect(wrapper.vm.div()).toBe(Infinity);
  });
});

describe('Float operations, string operands: "52" and "12.2"', () => {
  const wrapper = mount(Calculator);
  wrapper.vm.resetInitData();

  wrapper.setData({
    leftOperand: "52",
    inputValue: "12.2",
  });

  it('add operation', () => {
    expect(wrapper.vm.add()).toBe(64.2)
  });
  it('sub operation', () => {
    expect(wrapper.vm.sub()).toBe(39.8)
  });
  it('mul operation', () => {
    expect(wrapper.vm.mul()).toBe(634.4)
  });
  it('div operation', () => {
    expect(wrapper.vm.div()).toBe(52 / 12.2)
  });
});

describe('null operand behaviour: "null" and "11"', () => {
  const wrapper = mount(Calculator);
  wrapper.vm.resetInitData();

  wrapper.setData({
    leftOperand: null,
    inputValue: 11,
  });

  it('check null var', () => {
    expect(wrapper.vm.$data.leftOperand).toBeNull();
  });
  it('add operation', () => {
    expect(wrapper.vm.add()).toBe(NaN)
  });
  it('sub operation', () => {
    expect(wrapper.vm.sub()).toBe(NaN)
  });
  it('mul operation', () => {
    expect(wrapper.vm.mul()).toBe(NaN)
  });
  it('div operation', () => {
    expect(wrapper.vm.div()).toBe(NaN)
  });
});

describe('Undefined operand behaviour: "undefined" and "11"', () => {
  const wrapper = mount(Calculator);
  wrapper.vm.resetInitData();

  wrapper.setData({
    leftOperand: undefined,
    inputValue: 11,
  });

  it('Why does it NaN and not undefined?', () => {
    expect(wrapper.vm.$data.leftOperand).toBeNaN();
  });

  wrapper.vm.convertValuesToFloat();
  it('check that variable is NaN', () => {
    expect(wrapper.vm.$data.leftOperand).toBeNaN();
  });

  it('add operation', () => {
    expect(wrapper.vm.add()).toBeNaN()
  });
  it('sub operation', () => {
    expect(wrapper.vm.sub()).toBeNaN()
  });
  it('mul operation', () => {
    expect(wrapper.vm.mul()).toBeNaN()
  });
  it('div operation', () => {
    expect(wrapper.vm.div()).toBeNaN()
  });
});
