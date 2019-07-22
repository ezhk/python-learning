<template>
    <div class="interface">
        <input type="text" class="form-control" id="inputNumber"
               @change="validateInput" v-model="inputValue">
        <p class="suggest">{{leftOperand}} {{mathOperation}} {{inputValue}}</p>

        <div class="calculator-buttons">
            <div class="calculator-digests">
                <div class="calculator-numbers">
                    <button v-for="item of [1,2,3]" :key="item"
                            type="button" class="btn btn-outline-secondary"
                            @click.prevent="inputValue += item.toString()">{{item}}
                    </button>
                </div>
                <div class="calculator-numbers">
                    <button v-for="item of [4,5,6]" :key="item"
                            type="button" class="btn btn-outline-secondary"
                            @click.prevent="inputValue += item.toString()">{{item}}
                    </button>
                </div>
                <div class="calculator-numbers">
                    <button v-for="item of [7,8,9]" :key="item"
                            type="button" class="btn btn-outline-secondary"
                            @click.prevent="inputValue += item.toString()">{{item}}
                    </button>
                </div>
                <div class="calculator-numbers">
                    <button type="button" class="btn btn-danger"
                            @click="resetInitData">C
                    </button>
                    <button type="button" class="btn btn-outline-secondary"
                            @click.prevent="inputValue += '0'">0
                    </button>
                    <button type="button" class="btn btn-outline-secondary"
                            @click.prevent="inputValue += '.'">.
                    </button>
                </div>
            </div>

            <div class="calculator-operations">
                <button type="button" class="mathButtons btn btn-secondary"
                        @click.prevent="mathEventAction('add')">+
                </button>
                <button type="button" class="mathButtons btn btn-secondary"
                        @click.prevent="mathEventAction('sub')">-
                </button>
                <button type="button" class="mathButtons btn btn-secondary"
                        @click.prevent="mathEventAction('mul')">*
                </button>
                <button type="button" class="mathButtons btn btn-secondary"
                        @click.prevent="mathEventAction('div')">/
                </button>
            </div>
        </div>
        <button type="button" class="mathButtons resultButton btn btn-success"
                @click.prevent="result">=
        </button>
    </div>
</template>

<script>
  export default {
    name: "Calculator",
    data() {
      return {
        leftOperand: null,
        inputValue: '',
        mathOperation: null,
        inputRegexp: /^\d+(\.\d+)?$/i,
      }
    },
    methods: {
      /**
       * Проверяем вводимые символы по клику, допустимы лишь float.
       * Если значение != regexp, делаем неактивными кнопки и подсвечиваем поле ввода.
       */
      validateInput() {
        if (!this.inputValue.match(this.inputRegexp)) {
          document.querySelectorAll('.mathButtons').forEach(el => el.disabled = true);
          document.querySelector('input').classList.add('error-input');
        } else {
          document.querySelectorAll('.mathButtons').forEach(el => el.disabled = false);
          document.querySelector('input').classList.remove('error-input');
        }
      },

      /**
       * Сбрасываем data на изначальные
       */
      resetInitData() {
        Object.assign(this.$data, this.$options.data.apply(this));
      },

      /**
       * Если у нас уже есть актвная предыдущая операция.
       * необходимо её завершить (найти её результат).
       * Также проверяем необходимую переменную = тому, что ввел пользователь.
       */
      checkExistsValues() {
        if (this.inputValue === '') {
          throw new Error('input value must be defined');
        }
        if (this.mathOperation) {
          this.result();
        }
      },

      /**
       * Конвернтируем числовые операнды во float, перед вычислением.
       * Если формат невалидный (NaN), то возвращаем его;
       *     дополнительная валидация сделана в input.
       */
      convertValuesToFloat() {
        this.leftOperand = parseFloat(this.leftOperand);
        this.inputValue = parseFloat(this.inputValue);
      },

      /**
       * Действие по слику математического операнла: -, +, *, /.
       * Здесь проверяется, что предыдущая операция завершена и
       * сдвигается введеный операнд как его левое числовое значение
       * @param action, string
       */
      mathEventAction(action) {
        if (this.isUnaryOperator(action)) {
          return false;
        }
        this.checkExistsValues();
        this.mathOperation = action;
        this.leftOperand = this.inputValue;
        this.inputValue = '';
      },

      /**
       * Функиця определяет является ли операция не математематической,
       *   а добавлением унарного минуса или плюса:
       *   минус ставим если пустое число и нажата кнопка -;
       *   плюс ставим, если уже есть минус и нажат либо +, либо -.
       */
      isUnaryOperator(action) {
        if (this.inputValue === '' && action === 'sub') {
          this.inputValue += '-';
          return true;
        }

        if (this.inputValue === '-' &&
            (action === 'sub' || action === 'add')) {
          this.inputValue = '';
          return true;
        }

        return false;
      },

      /**
       * Набор математических методов,
       * которые производят операцию над двумя числовыми операндами
       */
      add() {
        this.convertValuesToFloat();
        return this.leftOperand + this.inputValue;
      },
      sub() {
        this.convertValuesToFloat();
        return this.leftOperand - this.inputValue;
      },
      mul() {
        this.convertValuesToFloat();
        return this.leftOperand * this.inputValue;
      },
      div() {
        this.convertValuesToFloat();
        return this.leftOperand / this.inputValue;
      },

      /**
       * По нажатию на = вызываем соответствующую математическую функцию
       * и сохраняем результата как inputValue.
       */
      result() {
        const calculateValue = this[this.mathOperation]();
        this.resetInitData();

        this.inputValue = calculateValue;
      },
    },
  }
</script>

<style scoped>
    * {
        margin: 0 auto;
        padding: 0;
    }

    .interface {
        display: flex;
        flex-direction: column;

        width: 400px;
    }

    .suggest {
        height: 1rem;
        font-size: 0.8rem;
    }

    .interface {
        display: flex;
        width: 210px;
        align-items: center;
        border: 1px solid darkgray;
        border-radius: 5px;
        padding: 3px;
    }

    input {
        padding: 5px;
    }

    .error-input {
        border-color: orangered;
    }

    button {
        margin: 5px;
        width: 40px;
        height: 40px;
    }

    .resultButton {
        width: 90px !important;
    }

    .calculator-buttons {
        display: flex;
        justify-content: center;
    }

    .calculator-operations {
        display: flex;
        flex-direction: column;
    }
</style>