# Clarify First — Confirmation Format Patterns

> **Version**: 1.3.0  
> **Last Updated**: 2026-03-11  
> **Compatibility**: Matches clarify-first/SKILL.md v1.3.0 (compact default clarification output + expanded form for high-risk execution)

Use these examples when shaping the user-facing confirmation output. The goal is not only to pause execution, but to make the pause easy to understand and easy to answer.

## Design Goal

1. Show only the facts that matter for the next decision.
2. Keep the user moving with 1-2 clear options.
3. Avoid overwhelming the user with protocol jargon unless the situation truly needs it.
4. Avoid tables and internal audit labels in the compact default form.
5. Mirror the user's language. Do not mix Chinese and English in the same heading.

## Default Compact Structure

### English

1. `Risk`
2. `Confirmed`
3. `Need From You`
4. `Options`
5. `Next Step`

### Chinese

1. `风险`
2. `我已确认`
3. `还需确认`
4. `可选方案`
5. `下一步`

## Example: Ambiguous Implementation Request (English)

```markdown
**[Risk: Medium | Trigger: scope-ambiguity | Confidence: 68% | Plan-ID: pending]** - I can continue, but I would be guessing about the target scope.

**Confirmed**
- You want the login flow improved.
- You want a real fix, not just an explanation.

**Need From You**
- Should I limit the change to `auth.ts`, or can I update related auth files too?
- Is this for local development or a production issue review?

**Options**
- **Option A (Recommended)**: Confirm scope first, then implement. Tradeoff: slower now, safer overall.
- **Option B**: I do a read-only diagnosis first. Tradeoff: faster now, but no code changes yet.

**Next Step**
- Reply with: `A + local development`.
```

## Example: 模糊开发请求（中文）

```markdown
**[风险：中 | 触发：scope-ambiguity | 确信度：66% | 计划ID：pending]** - 继续执行会带入关键范围假设。

**我已确认**
- 您要处理的是登录流程。
- 您希望真正修好，不是只做解释。

**还需确认**
- 是只改 `auth.ts`，还是允许联动其他认证文件？
- 这是本地开发问题，还是线上问题复盘？

**可选方案**
- **方案 A（推荐）**：先锁定范围，再改代码。取舍：更稳，但会多一次确认。
- **方案 B**：先做只读排查。取舍：更快，但暂时不改代码。

**下一步**
- 请回复：`A + 本地开发`。
```

## Example: High-Risk Request (Still Compact First)

```markdown
**[Risk: High | Trigger: destructive-op | Confidence: 54% | Plan-ID: pending]** - This is destructive and the environment is still unconfirmed.

**Confirmed**
- You want old data removed.
- This could affect production data.

**Need From You**
- Is this production, staging, or local?
- Do you want soft delete or hard delete?
- Do you already have a rollback path?

**Options**
- **Option A (Recommended)**: Verify scope and rollback first. Tradeoff: slower, much safer.
- **Option B**: I only prepare a safe review query first. Tradeoff: fastest, but no deletion yet.

**Next Step**
- Reply with: `A + staging + soft delete`.
```

## Example: 中文高频场景（产品/运营同学也能看懂）

```markdown
**[风险：中 | 触发：scope-ambiguity | 确信度：71% | 计划ID：pending]** - 我知道您想“优化”，但现在还不够确定要优化哪一部分。

**我已确认**
- 您希望把当前页面做得更好。
- 您希望我先对齐，再动代码。

**还需确认**
- 您更在意哪一项：加载速度、页面样式，还是转化效果？
- 范围是只改当前页面，还是允许联动相关组件？

**可选方案**
- **方案 A（推荐）**：先确定目标和范围，再实施。取舍：会多一次确认，但结果更稳。
- **方案 B**：我先做只读检查，给您一份问题清单。取舍：更快，但这一步不改代码。

**下一步**
- 请回复：`A + 加载速度 + 只改当前页面`。
```

## Example: 中文非技术场景（需求表达很口语）

```markdown
**[风险：中 | 触发：goal-ambiguity | 确信度：69% | 计划ID：pending]** - “帮我弄好”这个目标还不够具体，我现在继续会靠猜。

**我已确认**
- 您希望把这个问题真正处理好。
- 您不希望我先斩后奏。

**还需确认**
- 您说的“弄好”，是指修复报错、优化体验，还是补一个缺失功能？
- 这是线上正在影响用户的问题，还是本地开发中的问题？

**可选方案**
- **方案 A（推荐）**：您先选目标，我按目标执行。取舍：多一步确认，但方向不会跑偏。
- **方案 B**：我先做只读排查，帮您缩小范围。取舍：更省心，但暂时不改代码。

**下一步**
- 请回复：`A + 修复报错 + 线上问题`。
```

## Example: Chinese Detailed Version Only When Needed

```markdown
**[风险：高 | 触发：destructive-op | 确信度：58% | 计划ID：pending]** - 这是删除类操作，而且环境还没确认。

**我已确认**
- 您要清理旧数据。
- 这个动作可能影响线上数据。

**还需确认**
- 环境是生产、测试，还是本地？
- 您要软删除还是硬删除？
- 当前有没有可用回滚方案？

**可选方案**
- **方案 A（推荐）**：先确认环境和回滚，再生成执行计划。取舍：更慢，但更安全。
- **方案 B**：我先只生成统计查询，不做删除。取舍：最快，但这一步不会改数据。

**下一步**
- 请回复：`A + 测试环境 + 软删除`。

---

如需详细版，我再展开：
- 回滚准备
- 影响文件/表清单
- 执行步骤
- 风险说明
```

## When To Expand Beyond Compact Form

Expand into the full audit/snapshot/plan structure only when:

1. The task is HIGH risk.
2. The task requires a multi-step execution plan.
3. A rollback strategy, impact matrix, or search log is important to the decision.
4. The user explicitly asks for a detailed version.

Otherwise, keep the user-facing answer in the compact structure only.
